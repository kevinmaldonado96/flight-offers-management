from flask import jsonify, Flask
from flask_cors import CORS
from .bluprints.actions import actions_blueprint
from .configuracion.configuracion import Config
from .errors.errors import ApiError
import logging

app = Config.init()

cors = CORS(app)

logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(actions_blueprint, url_prefix='/scores')


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3008, debug=True)
