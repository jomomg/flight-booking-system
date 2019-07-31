def success_(message, data=None):
    response = {
        'status': 'success',
        'message': message,
    }
    if data:
        response['data'] = data
    return response


def error_(message, data=None):
    response = {
        'status': 'error',
        'message': message,
    }
    if data:
        response['errors'] = data
    return response
