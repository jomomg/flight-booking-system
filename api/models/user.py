from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from .base import BaseModel


class User(BaseModel):
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(60), unique=True)
    _password = db.Column(db.String(128))
    passport_no = db.Column(db.String(20))

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
