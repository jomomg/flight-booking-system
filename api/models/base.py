import uuid
import base64
import datetime as dt

from app import db


def generate_key():
    """Generate a url-safe uuid to use a database primary key"""
    _uuid = uuid.uuid4().bytes
    safe_uuid = base64.urlsafe_b64encode(_uuid)
    return safe_uuid.decode().replace('=', '')


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.String(22),
        default=generate_key,
        primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class CommonTimeFieldsMixin:
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=dt.datetime.utcnow)
