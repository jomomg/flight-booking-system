from flask import request
from flask_restful import Resource

from api.utils.responses import success_
from api.schemas import UserSchema


class Register(Resource):
    def post(self):
        schema = UserSchema()
        user = schema.load_json(request.data)
        user.save()
        payload = schema.dump(user).data
        return success_('registration successful', data=payload), 201
