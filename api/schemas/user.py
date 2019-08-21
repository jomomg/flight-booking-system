from marshmallow import fields, post_load

from .base import BaseSchema
from api.models import User
from api.utils.validators import (
    email_validator,
    string_length_validator,
    validate_unique_field
)


class UserSchema(BaseSchema):
    first_name = fields.String(
        required=True,
        validate=string_length_validator(1))
    last_name = fields.String(
        required=True,
        validate=string_length_validator(1))
    full_name = fields.String(
        dump_only=True,
        validate=string_length_validator(1))
    email = fields.String(
        required=True,
        validate=([
            email_validator,
            validate_unique_field(User, 'email')]))
    password = fields.String(
        required=True,
        load_only=True,
        validate=string_length_validator(8))
    username = fields.String(
        required=True,
        validate=([
            string_length_validator(4),
            validate_unique_field(User, 'username')]))
    passport = fields.String(
        required=True,
        validate=validate_unique_field(User, 'passport'))

    @post_load
    def make_user_object(self, data):
        return User(**data)
