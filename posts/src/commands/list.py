from datetime import datetime
import json

from sqlalchemy import and_
import requests

from .base_command import BaseCommannd
from ..models.model import db, Post, PostSchema
from ..errors.errors import TokenError, UnauthorizedError, BadRequestError
from ..validations.validations import Validate


class List(BaseCommannd):
    def __init__(self, token, args):
        self.token = token
        self.validate = Validate(data={})
        self.owner = args.get('owner', None)
        self.route_id = args.get('routeId', None)
        self.expire = args.get('expire', None)

    def execute(self, **params):
        filters = []

        if not self.token:
            raise TokenError

        if not self.validate.validate_token(token=self.token):
            raise UnauthorizedError

        if self.owner == 'me':
            user_id = self.__get_user_id()
        else:
            user_id = self.owner
        '''
        if self.expire and self.expire == 'true':
            
            posts = db.session.query(Post).filter(
                and_(Post.expireAt <= datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                    Post.routeId == self.route_id,
                    Post.userId == user_id
                     )).all()
            
            schema = PostSchema(many=True)
            posts_data = schema.dump(posts)
            return posts_data

        elif self.expire and self.expire == 'false':
            
            posts = db.session.query(Post).filter(
                and_(Post.expireAt >= datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                     Post.routeId == self.route_id,
                     Post.userId == user_id
            )).all()
            
            schema = PostSchema(many=True)
            posts_data = schema.dump(posts)
            return posts_data
        else:

            posts = db.session.query(Post).filter(and_(True, *filters)).all()

            schema = PostSchema(many=True)
            posts_data = schema.dump(posts)
            return posts_data
        '''
        if self.expire:
            if self.expire == 'false':
                filters.append(Post.expireAt >= datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ"))
            elif self.expire == 'true':
                filters.append(Post.expireAt < datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ"))
            else:
                raise BadRequestError
        if self.route_id:
            filters.append(Post.routeId == self.route_id)
        if self.owner:
            filters.append(Post.userId == user_id)
        
        posts = db.session.query(Post).filter(and_(True, *filters)).all()

        schema = PostSchema(many=True)
        posts_data = schema.dump(posts)
        return posts_data

    def __get_user_id(self):
        response = requests.get("http://users:3000/users/me", headers={"Authorization": self.token})
        data = json.loads(response.content.decode("utf-8"))
        return data.get("id")
