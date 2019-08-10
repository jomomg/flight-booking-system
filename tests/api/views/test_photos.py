import io
import os

from flask import current_app


class TestPhotoUploads:
    """Tests for photo uploads"""

    url = 'api/v1/user/photo'

    def test_uploading_photo_succeeds(self, init_db, client, auth_header):
        file_data = io.BytesIO(b'test image')
        rv = client.post(
            self.url,
            data={'file': (file_data, 'test.jpg')},
            headers=auth_header)
        assert rv.status_code == 200

    def test_retrieving_uploaded_photo_succeeds(
            self, init_db, client, auth_header):
        file_data = io.BytesIO(b'test image')
        client.post(
            self.url,
            data={'file': (file_data, 'test.jpg')},
            headers=auth_header)
        rv = client.get(self.url, headers=auth_header)
        assert rv.status_code == 200
        assert rv.data == b'test image'

    def test_uploading_new_photo_updates_users_photo(
            self, init_db, client, auth_header):
        file_data = io.BytesIO(b'test image')
        client.post(
            self.url,
            data={'file': (file_data, 'test.jpg')},
            headers=auth_header)
        rv = client.get(self.url, headers=auth_header)
        assert rv.data == b'test image'

        file_data = io.BytesIO(b'test image 2')
        client.post(
            self.url,
            data={'file': (file_data, 'test_2.jpg')},
            headers=auth_header)
        rv = client.get(self.url, headers=auth_header)
        assert rv.data == b'test image 2'

    def test_uploading_photo_with_invalid_extension_fails(
            self, init_db, client, auth_header, from_json):
        file_data = io.BytesIO(b'test image')
        rv = client.post(
            self.url,
            data={'file': (file_data, 'test.pdf')},
            headers=auth_header)
        assert rv.status_code == 400
        assert from_json(rv.data)['message'] == \
            'invalid file extension, must be one of png, jpg, jpeg, gif'

    def test_uploading_oversize_photo_fails(
            self, init_db, client, auth_header):
        large_file = 'test_large.jpg'
        file_size = current_app.config['MAX_CONTENT_LENGTH'] * 2
        with open(large_file, 'wb') as file:
            file.truncate(file_size)
        with open(large_file, 'rb'):
            rv = client.post(
                self.url,
                data={'file': (large_file, 'test.jpg')},
                headers=auth_header)
            assert rv.status_code == 413
        os.remove(large_file)

    def test_retrieving_non_existent_photo_returns_404(
            self, init_db, client, auth_header, from_json):
        rv = client.get(self.url, headers=auth_header)
        assert rv.status_code == 404
        assert from_json(rv.data)['message'] == 'no photo found'

    def test_deleting_uploaded_photo_succeeds(self, client, auth_header):
        file_data = io.BytesIO(b'test image')
        client.post(
            self.url,
            data={'file': (file_data, 'test.jpg')},
            headers=auth_header)
        rv = client.delete(self.url, headers=auth_header)
        assert rv.status_code == 204
