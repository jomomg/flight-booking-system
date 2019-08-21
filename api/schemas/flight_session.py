from marshmallow import fields

from .base import BaseSchema
from .flight import FlightSchema


class FlightSessionSchema(BaseSchema):
    flight_id = fields.String(load_only=True)
    flight = fields.Nested(
        FlightSchema,
        dump_only=True)
    departure = fields.DateTime()
    arrival = fields.DateTime()
    delayed = fields.Boolean()
    canceled = fields.Boolean()
