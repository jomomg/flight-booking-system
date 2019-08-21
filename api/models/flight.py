from app import db
from .base import BaseModel, CommonTimeFieldsMixin


class Flight(BaseModel, CommonTimeFieldsMixin):
    __tablename__ = 'flights'

    number = db.Column(db.String(10), unique=True)
    origin = db.Column(db.String(60), nullable=False)
    destination = db.Column(db.String(60), nullable=False)
    aircraft = db.Column(db.String(60), nullable=False)
