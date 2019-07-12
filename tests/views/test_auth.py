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

    def test_user_registration_succeeds(
            self, init_db, client, to_json, from_json):
        response = client.post(self.url, data=to_json(self.user_data))
        assert response.status_code == 201
        res_data = from_json(response.data)
        assert res_data['status'] == 'success'
        assert res_data['data']['email'] == self.user_data['email']

    def test_invalid_email_format_is_rejected(
            self, init_db, client, to_json, from_json):
        user_data = self.user_data.copy()
        user_data['email'] = 'john.doe.yahoo.com'
        resp = client.post(self.url, data=to_json(user_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['errors']['email'][0] == 'invalid email address'

    def test_duplicate_values_for_unique_fields_are_rejected(
            self, init_db, client, to_json, from_json):
        client.post(self.url, data=to_json(self.user_data))
        resp = client.post(self.url, data=to_json(self.user_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        for field in ('username', 'email', 'passport'):
            assert res_data['errors'][field][0] == f'{field} already exists'

    def test_blank_fields_are_rejected(
            self, init_db, client, to_json, from_json):
        user_data = self.user_data.copy()
        user_data['first_name'] = ""
        resp = client.post(self.url, data=to_json(user_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['errors']['first_name'][0] == \
            'string must be at least 1 characters long'


class TestUserLogin:
    user_data = {
        "email": "john.doe@yahoo.com",
        "first_name": "John",
        "last_name": "Doe",
        "passport": "random3",
        "username": "john.doe",
        "password": "last_pass"
    }
    login_data = {
        'username': 'john.doe',
        'password': 'last_pass'
    }
    url = '/api/v1/auth/login'

    def register_user(self, client, to_json):
        url = 'api/v1/auth/register'
        client.post(url, data=to_json(self.user_data))

    def test_user_login_succeeds(
            self, client, to_json, from_json, init_db):
        self.register_user(client, to_json)
        resp = client.post(self.url, data=to_json(self.login_data))
        assert resp.status_code == 200
        res_data = from_json(resp.data)
        assert 'token' in res_data['data']
        assert res_data['message'] == 'login successful'

    def test_login_with_wrong_password_fails(
            self, client, init_db, to_json, from_json):
        self.register_user(client, to_json)
        login_data = self.login_data.copy()
        login_data['password'] = 'wrong'
        resp = client.post(self.url, data=to_json(login_data))
        assert resp.status_code == 401
        res_data = from_json(resp.data)
        assert res_data['message'] == 'invalid username or password'

    def test_login_with_invalid_username_fails(
            self, init_db, client, to_json, from_json):
        self.register_user(client, to_json)
        login_data = self.login_data.copy()
        login_data['username'] = 'wrong'
        resp = client.post(self.url, data=to_json(login_data))
        assert resp.status_code == 401
        res_data = from_json(resp.data)
        assert res_data['message'] == 'invalid username or password'

    def test_login_with_missing_username_field_fails(
            self, client, init_db, to_json, from_json):
        self.register_user(client, to_json)
        login_data = self.login_data.copy()
        login_data.pop('username')
        resp = client.post(self.url, data=to_json(login_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['message'] == 'username is required to login'

    def test_login_with_missing_password_field_fails(
            self, client, init_db, to_json, from_json):
        self.register_user(client, to_json)
        login_data = self.login_data.copy()
        login_data.pop('password')
        resp = client.post(self.url, data=to_json(login_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['message'] == 'password is required to login'

    def test_login_with_blank_password_field_fails(
            self, client, init_db, to_json, from_json):
        self.register_user(client, to_json)
        login_data = self.login_data.copy()
        login_data['password'] = ''
        resp = client.post(self.url, data=to_json(login_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['message'] == 'password is required to login'

    def test_login_with_blank_username_fields_fails(
            self, client, init_db, to_json, from_json):
        self.register_user(client, to_json)
        login_data = self.login_data.copy()
        login_data['username'] = ''
        resp = client.post(self.url, data=to_json(login_data))
        assert resp.status_code == 400
        res_data = from_json(resp.data)
        assert res_data['message'] == 'username is required to login'
