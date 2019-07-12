import os
import datetime as dt
from functools import wraps

import jwt
from flask import request

from api.utils.exceptions import AuthenticationError
from api.models import User


def create_token(user_claims):
    """Create JWT token"""
    secret_key = os.getenv('SECRET_KEY')
    expiration_time = int(os.getenv('JWT_EXPIRES', 60))
    payload = {
        'user_claims': user_claims,
        'exp': dt.datetime.utcnow() + dt.timedelta(minutes=expiration_time),
        'iat': dt.datetime.utcnow()
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_token(token):
    """Decode JWT token"""
    secret_key = os.getenv('SECRET_KEY')
    try:
        decoded = jwt.decode(token, secret_key, algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationError('token has expired')
    except jwt.exceptions.InvalidTokenError:
        raise AuthenticationError('invalid token')
    else:
        return decoded


def get_token():
    """Retrieve token from authorization header"""
    token_string = request.headers.get('Authorization')
    if not token_string:
        raise AuthenticationError('no token provided')
    if not token_string.startswith('Bearer '):
        raise AuthenticationError('token should be preceded by the keyword Bearer')
    if len(token_string.split() < 2):
        raise AuthenticationError('invalid authorization header')
    _, token = token_string.split()
    return token


def token_required(fn):
    """Decorator to ensure that a valid token is included in a request"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = get_token()
        decoded_token = decode_token(token)
        username = decoded_token['user_claims']['username']
        user = User.query.filter_by(username=username).first()
        setattr(request, 'user', user)
        return fn(*args, **kwargs)
    return decorated
