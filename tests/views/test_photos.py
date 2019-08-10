import io


class TestPhotoUploads:
    """Tests for photo uploads"""

    url = 'api/v1/user/photo'

    def test_uploading_photo_succeeds(self, init_db, client, auth_header):
        file_data = io.BytesIO(b'test image')
        resp = client.post(
            self.url,
            data={'file': (file_data, 'test.jpg')},
            headers=auth_header)
        assert resp.status_code == 200

    def test_uploading_new_photo_updates_users_photo(self):
        pass

    def test_uploading_photo_with_invalid_extension_fails(self):
        pass

    def test_retrieving_uploaded_photo_succeeds(self):
        pass

    def test_retrieving_non_existent_photo_returns_404(self):
        pass

    def test_deleting_uploaded_photo_succeeds(self):
        pass
