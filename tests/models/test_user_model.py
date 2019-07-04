class TestUserModel:
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@email.com',
        'username': 'john.doe',
        'password': 'pass_1234',
        'passport_no': 'PXA123456'
    }

    def test_save_user(self, init_db):
        pass
