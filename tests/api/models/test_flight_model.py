from api.models import Flight


class TestFLightModel:
    flight_data = {
        'number': 'LH 44',
        'origin': 'Nairobi',
        'destination': 'London',
        'aircraft': 'Airbus A320'
    }
    
    def test_saving_flight_works(self, init_db):
        old_count = len(Flight.query.all())
        Flight(**self.flight_data).save()
        new_count = len(Flight.query.all())
        assert new_count - old_count == 1
