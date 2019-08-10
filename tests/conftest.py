import os
import json

import pytest

from app import create_app, db
from config import config

from api.utils.token_authentication import create_token
from api.models import User

FLASK_ENV = 'testing'
os.environ['FLASK_ENV'] = FLASK_ENV


@pytest.fixture(scope='session')
def app():
    """Fixture for initializing the app context"""
    app = create_app(config[FLASK_ENV])
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def init_db(app):
    """Fixture for creating and dropping test database"""
    db.create_all()
    yield
    db.session.close()
    db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    yield app.test_client()


@pytest.fixture
def auth_header(init_db):
    """Returns an access token"""
    user_data = {
        'first_name': 'Jon',
        'last_name': 'Doe',
        'username': 'jon_doe',
        'email': 'jon_doe@test.com',
        'passport': '1234ABABA'
    }
    user = User(**user_data)
    user.save()
    token = create_token(user_data).decode('UTF-8')
    yield {'Authorization': f'Bearer {token}'}
    user.delete()


@pytest.fixture
def to_json():
    """Convert data into json"""
    def _to_json(data):
        return json.dumps(data)
    return _to_json


@pytest.fixture
def from_json():
    """Convert data from json to native python objects"""
    def _from_json(data):
        return json.loads(data)
    return _from_json
