from api.models import User


class TestUserModel:
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@email.com',
        'username': 'john.doe',
        'password': 'pass_1234',
        'passport': 'PXA123456'
    }

    def test_save_user(self, init_db):
        old_count = len(User.query.all())
        User(**self.user_data).save()
        new_count = len(User.query.all())
        assert new_count - old_count == 1

    def test_password_is_hashed(self, init_db):
        user = User(**self.user_data).save()
        assert user.password != self.user_data['password']

    def test_password_verification_works(self, init_db):
        user = User(**self.user_data).save()
        assert user.check_password('wrong_password') is False
        assert user.check_password(self.user_data['password']) is True

    def test_full_name_property_works(self, init_db):
        user = User(**self.user_data).save()
        first_name = self.user_data['first_name']
        last_name = self.user_data['last_name']
        assert user.full_name == first_name + ' ' + last_name
