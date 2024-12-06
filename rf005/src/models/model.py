import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()

class Publish(db.Model):
    __tablename__ = 'publish'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    postId = db.Column(db.String(100))
    userId = db.Column(db.String(100))
    routeId = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

class PublishSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Publish
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

class PublishGetJsonSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    userId = fields.String()
    postId = fields.String()
    routeId = fields.String()
    createdAt = fields.DateTime()
