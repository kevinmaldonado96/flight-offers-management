from flask import Flask, jsonify, make_response, request, Blueprint
from src.commands.get_post import GetPost
import logging

from src.validators.validator import ValidadorConsultas

operations_blueprint = Blueprint('operations', __name__)
validador = ValidadorConsultas()


@operations_blueprint.route('/rf005/posts/<string:postId>', methods=['GET'])
def get_post(postId):
    headers = request.headers
    token = request.headers.get('Authorization')
    logging.debug(token)

    if validador.validar_consulta(headers, token, postId):
        result = GetPost(postId, headers, token).execute()
        
    return jsonify({'data': result}), 200

@operations_blueprint.route('/rf005/ping', methods = ['GET'])
def health():
    return 'pong', 200
