from marshmallow import fields

from .base import BaseSchema


class SeatSchema(BaseSchema):
    number = fields.String()
    type = fields.String()
    seat_class = fields.String()
    aircraft = fields.String()
