from flask import Flask, jsonify, make_response, request, Blueprint
from src.commands.create import Create
from src.commands.list import List
from src.commands.get import Get
from src.commands.delete import Delete
from src.commands.reset import Reset
import logging

from src.validators.validator import ValidadorOfertas

operations_blueprint = Blueprint('operations', __name__)
validador = ValidadorOfertas()

@operations_blueprint.route('/offers', methods = ['POST'])
def create():
    data = request.get_json()
    headers = request.headers 

    if validador.validar_request_creacion(headers, data):
        result = Create(data, headers).execute()

    iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    return jsonify({'id': result.id, "userId": result.userId, "createdAt": result.createdAt.strftime(iso_format)}), 201

@operations_blueprint.route('/offers', methods = ['GET'])
def list():
    headers = request.headers
    logging.debug(headers)

    post = request.args.get('post', None)
    owner = request.args.get('owner', None)

    if validador.validar_listado(headers):
        result = List(post, owner, headers).execute()

    return make_response(result, 200)

@operations_blueprint.route('/offers/<string:offerId>', methods = ['GET'])
def get(offerId):
    headers = request.headers
    logging.debug(headers)

    if validador.validar_consulta(headers, offerId):
        result = Get(offerId).execute()

    return make_response(result, 200)

@operations_blueprint.route('/offers/<string:offerId>', methods = ['DELETE'])
def delete(offerId):
    headers = request.headers
    logging.debug(headers)

    if validador.validar_consulta(headers, offerId):
        result = Delete(offerId).execute()

    return jsonify({"msg": result}), 200

@operations_blueprint.route('/offers/ping', methods = ['GET'])
def health():
    return 'pong', 200

@operations_blueprint.route('/offers/reset', methods = ['POST'])
def reset():
    result = Reset().execute()

    return jsonify({'msg': result}), 200
