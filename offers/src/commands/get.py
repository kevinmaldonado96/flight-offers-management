from .base_command import BaseCommannd
from src.models.model import Offer, db, OfferSchema, OfferGetJsonSchema
from src.errors.errors import OfertaNoExiste
import requests

offers_schema = OfferSchema()

class Get(BaseCommannd):
    def __init__(self, offerId):
        self.offerId = offerId

    def execute(self):
        offer = db.session.query(Offer).filter(Offer.id == self.offerId).first()

        if offer is None:
            raise OfertaNoExiste

        schema = OfferGetJsonSchema()
        offer_data = schema.dump(offer)

        return offer_data
    