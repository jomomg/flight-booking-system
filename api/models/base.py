import uuid
import base64
import datetime as dt

from app import db
from api.utils.exceptions import NotFoundError


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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_or_404(cls, object_id):
        record = cls.query.get(object_id)
        if not record:
            raise NotFoundError(f'{cls.__name__.lower()} not found')
        return record


class CommonTimeFieldsMixin:
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=dt.datetime.utcnow)
