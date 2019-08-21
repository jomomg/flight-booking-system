class TestFlights:
    flight_data = {
        'number': 'LH 44',
        'origin': 'Nairobi',
        'destination': 'London',
        'aircraft': 'Airbus A320'
    }
    url = '/api/v1/flights'

    def test_creating_a_flight_succeeds(
            self, client, init_db, from_json, to_json, auth_header):
        rv = client.post(
            self.url,
            data=to_json(self.flight_data),
            headers=auth_header)
        assert rv.status_code == 201
        resp_data = from_json(rv.data)
        assert resp_data['message'] == 'flight created'

    def test_retrieving_all_flights_succeeds(
            self, client, auth_header, to_json, from_json, init_db):
        for i in range(3):
            self.flight_data['number'] = str(i) * 4
            client.post(
                self.url,
                data=to_json(self.flight_data),
                headers=auth_header)
        rv = client.get(self.url, headers=auth_header)
        assert rv.status_code == 200
        resp_data = from_json(rv.data)
        assert len(resp_data['data']) == 3
