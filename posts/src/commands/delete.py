from .base_command import BaseCommannd
from ..models.model import db, Post
from ..errors.errors import TokenError, UnauthorizedError, BadRequestError, NotFoundError
from ..validations.validations import Validate


class Delete(BaseCommannd):
    def __init__(self, post_id, token):
        self.post_id = post_id
        self.token = token
        self.validate = Validate(data={})

    def execute(self):
        if not self.token:
            raise TokenError

        if not self.validate.validate_token(token=self.token):
            raise UnauthorizedError

        if not self.validate.validate_post_id_uuid(post_id=self.post_id):
            raise BadRequestError

        result = Post.query.filter(
            Post.id == self.post_id
        ).first()

        if not result:
            raise NotFoundError

        db.session.delete(result)
        db.session.commit()
        return   {
            "msg": "la publicación fue eliminada"
        }
