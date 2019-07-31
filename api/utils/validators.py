import re

from marshmallow import ValidationError
from flask import current_app

from api.utils.helpers import get_file_extension


def email_validator(email):
    email_regex = r'^[a-zA-Z0-9-._]+@[a-zA-Z0-9-_]+\.[a-zA-Z]{3,5}$'
    if not re.match(email_regex, email):
        raise ValidationError('invalid email address')


def string_length_validator(length):
    def validate(string):
        if len(string) < length:
            raise ValidationError(
                f'string must be at least {length} characters long')
    return validate


def validate_unique_field(model, field):
    def validate(value):
        result = model.query.filter_by(**{field: value}).first()
        if result:
            raise ValidationError(f'{field} already exists')
    return validate


def is_valid_file_extension(filename):
    return '.' in filename and get_file_extension(filename) in \
        current_app.config['ALLOWED_FILE_EXTENSIONS']
