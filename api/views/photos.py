import os

from flask import request, current_app, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound

from api.utils.exceptions import ValidationError
from api.utils.validators import is_valid_file_extension
from api.utils.responses import success_, error_
from api.utils.token_authentication import token_required
from api.models import Photo


class PhotoUpload(Resource):
    """Resource class for the photo upload endpoint"""

    @token_required
    def post(self):
        """View function for handling photo uploads.

        Takes an image file as input and saves it in the filesystem. The
        most recently uploaded image is set as the user's default photo.

        Returns:
            If successful, returns a payload with the following attributes
              - status: success
              - message: file upload successful
            else, the following error response is returned
              - status: error
              - message: invalid file extension
        """

        if 'file' not in request.files:
            raise ValidationError('no file specified')
        file = request.files['file']
        if file and is_valid_file_extension(file.filename):
            photo = Photo().save()
            filename = f'{photo.id}_{secure_filename(file.filename)}'
            file_path = os.path.join(
                current_app.config['PHOTO_UPLOAD_FOLDER'],
                filename)
            file.save(file_path)
            photo.path = file_path
            photo.save()
            request.user.photo_id = photo.id
            request.user.save()
            return success_('photo upload successful')
        allowed_extensions = ', '.join(
            current_app.config['ALLOWED_FILE_EXTENSIONS'])
        return error_(
            f'invalid file extension, must be one of {allowed_extensions}'), 400

    @token_required
    def get(self):
        """Retrieves a user's photo.

        Returns:
            If successful, it returns the uploaded photo.
        """
        try:
            photo = request.user.photo
            if not photo:
                raise NotFound
            return send_from_directory(
                current_app.config['PHOTO_UPLOAD_FOLDER'],
                photo.path[8:])
        except NotFound:
            return error_('no photo found'), 404
