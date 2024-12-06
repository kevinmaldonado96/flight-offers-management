from flask import jsonify, Flask
from flask_cors import CORS
from .blueprints.blueprints import routes
from .configuracion.configuracion import Config
from .errors.errors import ApiError
import logging

app = Config.init()

cors = CORS(app)

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(routes, url_prefix='/routes')

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True)