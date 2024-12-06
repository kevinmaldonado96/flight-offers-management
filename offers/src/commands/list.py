from .base_command import BaseCommannd
from src.models.model import Offer, db, OfferSchema, OfferGetJsonSchema
from src.utils.utils import FileUtils
from sqlalchemy import and_
import uuid
import requests
from src.errors.errors import CamposFaltantes

offers_schema = OfferSchema()

class List(BaseCommannd):
    def __init__(self, post, owner, headers):
        self.post = post
        self.owner = owner
        self.token = headers

    def execute(self):
        filters = []
        user_id = FileUtils().get_user(self.token)

        if self.post:
            filters.append(Offer.postId == self.post)
        
        if self.owner:
            filters.append(Offer.userId == self.get_owner(self.owner, user_id))

        #offers = db.session.query(Offer).filter(and_(*filters)).all()
        offers = db.session.query(Offer).filter(and_(True, *filters)).all()
        schema = OfferGetJsonSchema(many=True)
        offers_data = schema.dump(offers)

        return offers_data
    
    def get_owner(self, owner, user_id):
        if owner == 'me':
            return user_id
        return owner
    
    def search_fields(self):
        print('Validando información para consultar ofertas')

        if self.owner and self.owner == 'me':
            return

        if self.owner:
            try:
                uuid.UUID(self.owner)
                return
            except ValueError:
                raise CamposFaltantes