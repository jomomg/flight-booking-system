from sqlalchemy.orm import backref

from app import db
from .base import BaseModel, CommonTimeFieldsMixin


class Photo(BaseModel, CommonTimeFieldsMixin):
    __tablename__ = 'photo'

    path = db.Column(db.String(255), unique=True)
    user = db.relationship('User',
                           backref=backref('photo', uselist=False),
                           lazy=True)
