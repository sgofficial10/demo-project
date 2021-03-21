from flask import jsonify


def get_error_response(message, error_code, **kwargs):
    resp = kwargs
    resp['message'] = message
    return jsonify(resp), error_code


def get_client_error_response(message='Invalid request', error_code=400, **kwargs):
    return get_error_response(message, error_code, **kwargs)


def get_server_error_response(message='Server error', error_code=500, **kwargs):
    return get_error_response(message, error_code, **kwargs)


def get_availability_response(availability, response_code=200):
    return jsonify({'exists': availability}), response_code


def get_success_response(message='Operation successful', data=None, response_code=200, **kwargs):
    resp = kwargs
    resp['message'] = message
    if data is not None:
        resp['data'] = data

    return jsonify(resp), response_code