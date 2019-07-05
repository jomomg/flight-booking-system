from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

from api import api as api_blueprint
from api.utils.exceptions import APIError


api = Api(api_blueprint)

db = SQLAlchemy()
migrate = Migrate()


@api_blueprint.errorhandler(APIError)
def handle_api_exceptions(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(api_blueprint)
    return app
