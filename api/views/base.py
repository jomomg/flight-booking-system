from flask import request
from flask_restful import Resource

from api.utils.responses import success_
from api.utils.token_authentication import token_required


class BaseResource(Resource):
    model = None
    schema_class = None
    post_success_msg = None
    get_success_msg = None
    authenticate = True

    @property
    def method_decorators(self):
        return [token_required] if self.authenticate else []

    @property
    def resource_name(self):
        return self.model.__name__.lower()


class BaseListResource(BaseResource):
    def post(self):
        schema = self.schema_class()
        instance_data = schema.load_json(request.data)
        instance = self.model(**instance_data)
        instance.save()
        response_data = schema.dump(instance).data
        msg = self.post_success_msg or f'{self.resource_name} created'
        return success_(msg, data=response_data), 201

    def get(self):
        schema = self.schema_class(many=True)
        instances = self.model.query.all()
        response_data = schema.dump(instances).data
        msg = self.get_success_msg or f'{self.resource_name}s fetched'
        return success_(msg, data=response_data), 200


class BaseDetailResource(BaseResource):
    def get(self, resource_id):
        pass

    def patch(self, resource_id):
        pass
