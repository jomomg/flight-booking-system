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


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from api import models
    from api import views

    flask_api.add_resource(views.Register, '/auth/register')
    flask_api.add_resource(views.Login, '/auth/login')
    flask_api.add_resource(views.PhotoUpload, '/user/photo')
    # flask_api.add_resource(views.FileUploadDetail, '/uploads/<photo_id>')

    app.register_blueprint(api_bp)
    return app
