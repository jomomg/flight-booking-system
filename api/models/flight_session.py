from app import db
from .base import BaseModel


class FlightSession(BaseModel):
    __tablename__ = 'flight_sessions'

    flight_id = db.Column(
        db.String(22),
        db.ForeignKey('flights.id'))
    departure = db.Column(db.DateTime)
    arrival = db.Column(db.DateTime)
    delayed = db.Column(
        db.Boolean,
        default=False)
    canceled = db.Column(
        db.Boolean,
        default=False)

    flight = db.relationship(
        'Flight',
        backref='flight_sessions',
        lazy=True)
    seats = db.relationship(
        'FlightSessionSeat',
        backref='flight_session',
        lazy=True)


class FlightSessionSeat(BaseModel):
    __tablename__ = 'flight_session_seats'

    flight_session_id = db.Column(
        db.String(22),
        db.ForeignKey('flight_sessions.id'))
    seat_id = db.Column(
        db.String(22),
        db.ForeignKey('seats.id'))
    seat = db.relationship(
        'Seat',
        backref='flight_sessions',
        lazy=True)
