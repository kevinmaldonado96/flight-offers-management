from flask import Blueprint, request, jsonify
from ..dto.response_dto import ResponseDTO
from ..commands.trayecto_existe import TrayectoExiste
from ..commands.crear_trayecto import CrearTrayecto
from ..commands.post_existe import PostExiste
from ..commands.crear_post import CrearPost
from ..validators.validators import Validador
import logging

controllers = Blueprint('rf003', __name__)
validador = Validador()

@controllers.route("/ping", methods=['GET'])
def ping():
    return "pong", 200

@controllers.route("/posts", methods=['POST'])
def creacion_post():

    es_route_nuevo = False

    headers = request.headers
    data = request.get_json()

    validador.validar_creacion_publicacion(data, headers)
    header_validaciones = obtener_header(headers)

    fligth_id = data["flightId"]

    trayecto_existe = TrayectoExiste(fligth_id, header_validaciones)
    id_trayecto = trayecto_existe.ejecutar()

    if id_trayecto is None:
        crear_trayecto = CrearTrayecto(data, header_validaciones)
        id_trayecto = crear_trayecto.ejecutar()
        es_route_nuevo = True

    post_existe = PostExiste(id_trayecto, header_validaciones)
    post_existe.ejecutar()

    fecha_expiracion = data["expireAt"]

    crear_post = CrearPost(id_trayecto, es_route_nuevo, fecha_expiracion, header_validaciones)
    response_publicaciones = crear_post.ejecutar()

    id_publicacion = response_publicaciones["id"]
    id_user = response_publicaciones["userId"]

    publicaciones_dto = ResponseDTO(id_publicacion, id_user, fecha_expiracion, id_trayecto)

    return publicaciones_dto.to_json(), 201


def obtener_header(headers):
    token_encabezado = headers.get('Authorization')
    logging.debug(f"token_encabezado {token_encabezado}")
    token_sin_bearer = token_encabezado[len('Bearer '):]
    logging.debug(f"token_sin_bearer {token_sin_bearer}")

    headers = {
         "Authorization": f"Bearer {token_sin_bearer}",
    }

    return headers
