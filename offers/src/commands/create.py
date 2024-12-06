from flask import jsonify, request
import requests
from .base_command import BaseCommannd
from src.models.model import Offer, db
from src.utils.utils import FileUtils

class Create(BaseCommannd):
    
    def __init__(self, data_offer, headers):
        self.token = headers
        self.postId = data_offer.get('postId')
        self.description = data_offer.get('description')
        self.size = data_offer.get('size')
        self.fragile = data_offer.get('fragile')
        self.offer = data_offer.get('offer')

    def execute(self):

        user_id = FileUtils().get_user(self.token)

        new_offer = Offer(
            postId=self.postId,
            userId=user_id,
            description=self.description,
            size=self.size,
            fragile=self.fragile,
            offer=self.offer
        )

        db.session.add(new_offer)
        db.session.commit()

        return new_offer
