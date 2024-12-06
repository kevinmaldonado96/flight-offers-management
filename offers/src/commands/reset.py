from .base_command import BaseCommannd
from src.models.model import Offer, db

class Reset(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        db.session.query(Offer).delete()
        db.session.commit()

        return "Todos los datos fueron eliminados"
    