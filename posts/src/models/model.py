import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    routeId = db.Column(db.String(100))
    userId = db.Column(db.String(100))
    expireAt = db.Column(db.DateTime())
    createdAt = db.Column(db.DateTime())

class PostSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    routeId = fields.String()
    userId = fields.String()
    expireAt = fields.DateTime()
    createdAt = fields.DateTime()