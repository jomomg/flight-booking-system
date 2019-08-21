from app import db
from .base import BaseModel, CommonTimeFieldsMixin


class Booking(BaseModel, CommonTimeFieldsMixin):
    __tablename__ = 'bookings'

    user_id = db.Column(db.String(22), db.ForeignKey('user.id'))
    flight_id = db.Column(db.String(22), db.ForeignKey('flights.id'))
    flight_session_id = db.Column(
        db.String(22),
        db.ForeignKey('flight_sessions.id'))
    seat_id = db.Column(db.String(22), db.ForeignKey('flight_session_seats.id'))
    flight_session = db.relationship('Booking', backref='bookings', lazy=True)
    seat = db.relationship('FlightSessionSeat', backref='bookings', lazy=True)
