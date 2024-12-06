import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()


class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = db.Column(db.String(50))
    createdAt = db.Column(db.DateTime())


class ScoreSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    value = fields.String()
    createdAt = fields.DateTime()