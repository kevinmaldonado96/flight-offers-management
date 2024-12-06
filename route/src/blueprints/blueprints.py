from flask import Blueprint, request, jsonify
from ..commands.trayecto_command import TrayectoCommand
from ..validators.validator import ValidadorTrayectos
from ..errors.errors import TrayectoNoExiste
import logging
import uuid

routes = Blueprint('routes', __name__)
validador = ValidadorTrayectos()

@routes.route('/', methods=['POST'])
def creacion_trayecto():

    data = request.get_json()
    headers = request.headers

    if validador.validar_request_creacion(data, headers):
        result = TrayectoCommand().crear_trayecto(data)

    iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    return jsonify({'id': result.id, "createdAt": result.createdAt.strftime(iso_format)}), 201

@routes.route('/', methods=['GET'])
def ver_trayectos():

    flight_id = request.args.get('flight')
    headers = request.headers

    logging.debug(headers)
    if validador.validar_consulta_flight(headers):
        result = TrayectoCommand().ver_trayetos_por_flightId(flight_id)
    return result

@routes.route('/<string:id>', methods=['GET'])
def ver_trayecto_por_id(id):

    headers = request.headers
    if validador.validar_consulta_por_id(id, headers):
        trayecto = TrayectoCommand().ver_trayetos_por_id(id)
        if not trayecto:
            raise TrayectoNoExiste
        else:
            return trayecto

@routes.route('/<string:id>', methods=['DELETE'])
def eliminar_trayecto(id):
    headers = request.headers
    if validador.validar_eliminar_por_id(id, headers):
        TrayectoCommand().eliminar_trayeto_por_id(id)
        return jsonify({'msg': "el trayecto fue eliminado"})

@routes.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@routes.route('/reset', methods=['POST'])
def reset():
    TrayectoCommand().reset()
    return jsonify({'msg': "el trayecto fue eliminado"})