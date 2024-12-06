from .base_command import BaseCommannd
from ..models.model import db, Post

class Reset(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        try:
            db.session.query(Post).delete()
        except Exception as e:
            raise e
        else:
            db.session.commit()
            return {'msg': "Todos los datos fueron eliminados"}
