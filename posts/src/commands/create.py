from datetime import datetime
import pytz
import json

import requests

from .base_command import BaseCommannd
from ..models.model import db, Post
from ..errors.errors import TokenError, UnauthorizedError, BadRequestError
from ..errors.errors import DateTypeError
from ..validations.validations import Validate


class Create(BaseCommannd):
    def __init__(self, data, token):
        self.data = data
        self.validate = Validate(data=self.data)
        self.token = token

    def execute(self):
        if self.token is None:
            raise TokenError

        if not self.validate.validate_token(token=self.token):
            raise UnauthorizedError

        if not self.validate.validate_data():
            raise BadRequestError

        if not self.validate.validate_date_field():
            raise DateTypeError

        new_post = self.__create_new_post()

        return {
            "id": new_post.id,
            "userId": self.get_user_id(),
            "createdAt": new_post.createdAt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

    def get_user_id(self):
        response = requests.get("http://users:3000/users/me", headers={"Authorization": self.token})
        data = json.loads(response.content.decode("utf-8"))
        return data["id"]

    @staticmethod
    def __set_utc(raw_date):
        timezone = pytz.timezone("UTC")
        new = timezone.localize(raw_date)
        return new

    def __get_expired_at_date(self):
        return self.__set_utc(
            raw_date=datetime.strptime(self.data.get("expireAt"), "%Y-%m-%dT%H:%M:%S.%fZ")
        )

    def __create_new_post(self):
        try:
            new_post = Post(
                routeId=self.data.get('routeId'),
                userId=self.get_user_id(),
                expireAt=self.__get_expired_at_date(),
                #createdAt=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                createdAt=datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ")
            )
        except Exception as e:
            raise e
        else:
            db.session.add(new_post)
            db.session.commit()
            return new_post

