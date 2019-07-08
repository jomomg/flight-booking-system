class TestUserRegistration:
    user_data = {
        "email": "john.doe@yahoo.com",
        "first_name": "John",
        "last_name": "Doe",
        "passport": "random3",
        "username": "john.doe",
        "password": "last_pass"
    }
    url = 'api/v1/auth/register'

    def test_user_registration_succeeds(self, init_db, client, to_json, from_json):
        response = client.post(self.url, data=to_json(self.user_data))
        assert response.status_code == 201
        res_data = from_json(response.data)
        assert res_data['status'] == 'success'
        assert res_data['data']['email'] == self.user_data['email']

    def test_duplicate_values_for_unique_fields_are_rejected(
            self, init_db, client, to_json, from_json):
        client.post(self.url, data=to_json(self.user_data))
        resp = client.post(self.url, data=to_json(self.user_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        for field in ('username', 'email', 'passport'):
            assert res_data['errors'][field][0] == f'{field} already exists'

    def test_blank_fields_are_rejected(self, init_db, client, to_json, from_json):
        user_data = self.user_data.copy()
        user_data['first_name'] = ""
        resp = client.post(self.url, data=to_json(user_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['errors']['first_name'][0] == 'string must be at least 1 characters long'
