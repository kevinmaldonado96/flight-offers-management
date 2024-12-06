import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Trayecto(db.Model):
    __tablename__ = 'trayecto'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    flightId = db.Column(db.String)
    sourceAirportCode = db.Column(db.String(3))
    sourceCountry = db.Column(db.String)
    destinyAirportCode = db.Column(db.String(3))
    destinyCountry = db.Column(db.String)
    bagCost = db.Column(db.Integer)
    plannedStartDate = db.Column(db.DateTime(timezone=True))
    plannedEndDate = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, onupdate=datetime.utcnow)

class TrayectosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trayecto
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
   # createdAt = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ')