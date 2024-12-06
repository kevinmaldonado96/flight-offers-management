import os

from flask import Flask, jsonify, request, Blueprint, make_response

from ..commands.calculate import Calculate


actions_blueprint = Blueprint('operations', __name__)


@actions_blueprint.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    result = Calculate(data=data, token=request.headers.get('Authorization')).execute()
    return jsonify(result), 201


@actions_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200
