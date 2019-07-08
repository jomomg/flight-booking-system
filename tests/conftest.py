import os
import json

import pytest

from app import create_app, db
from config import config

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


@pytest.fixture(scope='function')
def init_db(app):
    """Fixture for creating and dropping test database"""
    db.create_all()
    yield
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Test client"""
    yield app.test_client()


@pytest.fixture(scope='function')
def to_json():
    """Convert data into json"""
    def _to_json(data):
        return json.dumps(data)
    return _to_json


@pytest.fixture(scope='function')
def from_json():
    """Convert data from json to native python objects"""
    def _from_json(data):
        return json.loads(data)
    return _from_json
