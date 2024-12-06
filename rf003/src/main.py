from flask import jsonify, Flask
from flask_cors import CORS
from .blueprints.blueprints import controllers
from .errors.errors import Rf003Exception
from dotenv import load_dotenv
import logging

app = Flask(__name__) 

cors = CORS(app)

load_dotenv('.env.template')

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(controllers, url_prefix='/rf003')

app_context = app.app_context()
app_context.push()

@app.errorhandler(Rf003Exception)
def handle_exception(err):
    response = {
      "msg": err.message
    }
    return jsonify(response), err.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3006, debug=True)