from marshmallow import fields

from .base import BaseSchema


class FlightSchema(BaseSchema):
    number = fields.String()
    origin = fields.String()
    destination = fields.String()
    aircraft = fields.String()
