import uuid
import os
import json
from datetime import datetime

import requests


class Validate:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def validate_token(token):
        response = requests.get(f"{os.getenv('USERS_PATH')}/users/me", headers={"Authorization": token})
        if response.status_code == 200:
            return True
        else:
            return False


    def validate_data(self):
        route_id = self.data.get("routeId")
        expire_at = self.data.get("expireAt")

        if route_id and expire_at:
            if isinstance(route_id, str) and isinstance(expire_at, str):
                if bool(datetime.strptime(self.data.get("expireAt"), "%Y-%m-%dT%H:%M:%S.%fZ")):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def validate_date_field(self):
        raw_date = datetime.strptime(self.data.get("expireAt"), "%Y-%m-%dT%H:%M:%S.%fZ")
        now_iso_format = datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ")
        validated_date = bool(datetime.strptime(self.data.get("expireAt"), "%Y-%m-%dT%H:%M:%S.%fZ"))

        if raw_date > now_iso_format and validated_date:
            return True
        else:
            return False

    @staticmethod
    def validate_post_id_uuid(post_id):
        if isinstance(post_id, str):
            try:
                uuid.UUID(str(post_id))
                return True
            except ValueError:
                return False
        else:
            return False