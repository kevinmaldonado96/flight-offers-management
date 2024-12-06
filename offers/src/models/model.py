import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()

class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    postId = db.Column(db.String(100))
    userId = db.Column(db.String(100))
    description = db.Column(db.String(100))
    size = db.Column(db.String(100))
    fragile = db.Column(db.Boolean)
    offer = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

class OfferSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Offer
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

class OfferGetJsonSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    postId = fields.String()
    description = fields.String()
    size = fields.String()
    fragile = fields.Boolean()
    offer = fields.Integer()
    createdAt = fields.DateTime()
    userId = fields.String()
