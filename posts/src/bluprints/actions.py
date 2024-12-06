import os

from flask import Flask, jsonify, request, Blueprint, make_response

from ..commands.create import Create
from ..commands.delete import Delete
from ..commands.list import List
from ..commands.retrieve import Retrieve
from ..commands.reset import Reset

actions_blueprint = Blueprint('operations', __name__)

@actions_blueprint.route('/', methods = ['POST'])
def create():
    data = request.get_json()
    result = Create(data=data, token=request.headers.get('Authorization')).execute()
    return jsonify(result), 201

@actions_blueprint.route('/', methods = ['GET'])
def list_filter():
    result = List(token=request.headers.get('Authorization'), args=request.args).execute()
    return jsonify(result), 200

@actions_blueprint.route('/<string:post_id>', methods = ['GET'])
def retrieve(post_id):
    result = Retrieve(post_id=post_id, token=request.headers.get('Authorization')).execute()
    return make_response(result, 200)


@actions_blueprint.route('/<string:post_id>', methods = ['DELETE'])
def delete(post_id):
    result = Delete(post_id=post_id, token=request.headers.get('Authorization')).execute()
    return make_response(result, 200)


@actions_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@actions_blueprint.route('/reset', methods=['POST'])
def reset():
    result = Reset().execute()
    return jsonify(result)