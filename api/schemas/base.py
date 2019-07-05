from marshmallow import Schema, fields

from api.utils.exceptions import ValidationError


class BaseSchema(Schema):
    id = fields.String(dump_only=True)

    def load_json(self, data):
        """
        Deserialize JSON data and return a model object.
        Raises a ValidationError exception if an error is encountered
        during deserialization.
        """
        result, errors = self.loads(data)
        if errors:
            raise ValidationError(data=errors)
        else:
            return result
