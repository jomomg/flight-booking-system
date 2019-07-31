from api.utils.responses import error_


class APIError(Exception):
    message = 'an error occurred'
    status_code = 400

    def __init__(self, message=None, data=None, status_code=None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.data = data

    def to_dict(self):
        return error_(self.message, self.data)


class ValidationError(APIError):
    message = 'a validation error occurred'
    status_code = 400


class AuthenticationError(APIError):
    message = 'invalid authentication credentials'
    status_code = 401


class NotFoundError(APIError):
    message = 'object not found'
    status_code = 404
