from flask import Flask
from flask_restful import Api

from api import api as api_blueprint


api = Api(api_blueprint)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(api_blueprint)
    return app
