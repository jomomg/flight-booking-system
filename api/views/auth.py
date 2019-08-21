import json

from flask import request
from flask_restful import Resource

from api.utils.responses import success_
from api.utils.exceptions import ValidationError, AuthenticationError
from api.utils.token_authentication import create_token
from api.schemas import UserSchema
from api.models import User

from .base import BaseListResource


class Register(BaseListResource):
    model = User
    schema_class = UserSchema
    authenticate = False


class Login(Resource):
    def post(self):
        if not request.data:
            raise ValidationError(
                'login credentials are required')
        login_details = json.loads(request.data)
        username = login_details.get('username')
        password = login_details.get('password')
        if not username:
            raise ValidationError('username is required to login')
        if not password:
            raise ValidationError('password is required to login')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            schema = UserSchema(exclude=('passport', 'password'))
            payload = {'token': create_token(schema.dump(user).data).decode()}
            return success_('login successful', data=payload), 200
        else:
            raise AuthenticationError('invalid username or password')
