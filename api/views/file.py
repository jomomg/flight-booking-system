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


class FileUploadList(Resource):
    """Resource class for the file upload endpoint"""

    @token_required
    def post(self):
        """View function for handling file uploads

        Takes an image file as input and saves it in the filesystem

        Returns:
            If successful, returns a payload with the following attributes
              - filename: the filename of the uploaded file
              - file_url: the url that can be used to retrieve the file
            else, the following error response is returned
              - status: error
              - message: invalid file extension
        """

        if 'file' not in request.files:
            raise ValidationError('no file specified')
        file = request.files['file']
        if file and is_valid_file_extension(file.filename):
            filename = f'{request.user.id}_{secure_filename(file.filename)}'
            file_path = os.path.join(
                current_app.config['PHOTO_UPLOAD_FOLDER'],
                filename)
            file.save(file_path)
            photo = Photo(path=file_path)
            photo.save()
            request.user.photo_id = photo.id
            request.user.save()
            ret = {
                'filename': filename,
                'file_url': f'{request.url_root}uploads/{filename}'
            }
            return success_('file upload successful', data=ret)
        return error_('invalid file extension'), 400


class FileUploadDetail(Resource):
    """Resource class foe retrieving an uploaded file"""

    @token_required
    def get(self, filename):
        """Retrieves an uploaded file

        Args:
            filename (str): filename of the file to be retrieved

        Returns:
            If successful, it returns the uploaded file
        """

        try:
            return send_from_directory(
                current_app.config['PHOTO_UPLOAD_FOLDER'],
                filename)
        except NotFound:
            return error_('file not found'), 404
