from datetime import datetime
import pytz
import json

import requests
import logging

from .base_command import BaseCommannd
from ..models.model import db, Score
from ..errors.errors import TokenError, UnauthorizedError, BadRequestError
from ..errors.errors import DateTypeError
from ..validations.validations import Validate


class Calculate(BaseCommannd):
    def __init__(self, data, token):
        self.data = data
        self.validate = Validate(data=self.data)
        self.token = token

    def execute(self):

        if self.token is None:
            raise TokenError

        if not self.validate.validate_token(token=self.token):
            raise UnauthorizedError

        if not self.data.get('offer') or not self.data.get('size') or not self.data.get('bagCost'):
            raise BadRequestError

        if self.data.get('size') == 'SMALL':
            size = 0.25
        elif self.data.get('size') == 'MEDIUM':
            size = 0.5
        else:
            size = 1

        value = (float(self.data.get("offer")) - ((float(size) * float(self.data.get('bagCost')))))

        return {
            "value": value
        }
