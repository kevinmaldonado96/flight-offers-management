import os
import time
import logging
from os import environ

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError
from .models.model import db
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv('.env.template')

app_context = app.app_context()
app_context.push()

logging.basicConfig(level=logging.DEBUG) 

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code

app.register_blueprint(operations_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3005, debug=True)