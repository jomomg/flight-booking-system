from app import db
from .base import BaseModel, CommonTimeFieldsMixin


class Seat(BaseModel):
    __tablename__ = 'seats'

    number = db.Column(db.String(10), unique=True)
    type = db.Column(db.String(20))
    seat_class = db.Column(db.String(60), nullable=False)
    aircraft = db.Column(db.String(60), nullable=False)
