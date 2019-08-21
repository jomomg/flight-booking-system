from marshmallow import fields

from .base import BaseSchema
from .user import UserSchema
from .flight import FlightSchema
from .flight_session import FlightSessionSchema
from .seat import SeatSchema


class BookingSchema(BaseSchema):
    user = fields.Nested(
        UserSchema,
        exclude=('username',),
        dump_only=True)
    flight_session_id = fields.String(load_only=True)
    flight_session = fields.Nested(
        FlightSessionSchema,
        exclude=('flight',),
        dump_only=True)
    flight = fields.Nested(
        FlightSchema,
        dump_only=True)
    seat_id = fields.String(load_only=True)
    seat = fields.Nested(
        SeatSchema,
        exclude=('aircraft',),
        dump_only=True)
