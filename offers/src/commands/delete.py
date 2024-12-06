from .base_command import BaseCommannd
from src.models.model import Offer, db, OfferSchema
from src.errors.errors import OfertaNoExiste

offers_schema = OfferSchema()

class Delete(BaseCommannd):
    def __init__(self, offerId):
        self.offerId = offerId

    def execute(self):
        offer = db.session.query(Offer).filter(Offer.id == self.offerId).first()

        if offer is None:
            raise OfertaNoExiste

        db.session.delete(offer)
        db.session.commit()

        return "la oferta fue eliminada"
    