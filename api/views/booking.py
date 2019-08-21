from flask_restful import Resource


class Booking(Resource):
    def post(self):
        pass

    def get(self):
        pass


class BookingDetail(Resource):
    def patch(self, booking_id):
        pass

    def delete(self, booking_id):
        pass
