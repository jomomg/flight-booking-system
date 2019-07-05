def success_(message, data):
    response = {
        'status': 'success',
        'message': message,
        'data': data
    }
    return response


def error_(message, data=None):
    response = {
        'status': 'error',
        'message': message,
    }
    if data:
        response['errors'] = data
    return response
