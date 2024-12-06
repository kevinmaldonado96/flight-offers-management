import os
import time
from flask import Flask
from ..models.model import db
from dotenv import load_dotenv


class Config:
    @staticmethod
    def init():
        app = Flask(__name__)
        load_dotenv('.env.template')
        '''
        db_url = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_url}"

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config["PROPAGATE_EXCEPTIONS"] = True

        db.init_app(app)
        db.create_all()
        '''

        app_context = app.app_context()
        app_context.push()
        return app
