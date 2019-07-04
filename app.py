from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

from api import api as api_blueprint


api = Api(api_blueprint)

db = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(api_blueprint)
    return app
