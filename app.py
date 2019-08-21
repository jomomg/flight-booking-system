from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

from api import api_bp
from api.utils.exceptions import APIError


flask_api = Api(api_bp)

db = SQLAlchemy()
migrate = Migrate()


@api_bp.errorhandler(APIError)
def handle_api_exceptions(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def register_urls(urls):
    for url in urls:
        flask_api.add_resource(*url)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from api import models
    from api import views

    register_urls(views.URLS)

    app.register_blueprint(api_bp)
    return app
