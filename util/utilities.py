import json
import random
import re


def has_allowed_keys(data, accepted_keys):
    """
    Returns if data contains any keys that is not present in accepted_keys
    :param data: The object to be verified. Must be dict
    :param accepted_keys: The list of keys allowed.
    :return: boolean: Result of the verification.
    """
    if data is None:
        return False

    for key in data.keys():
        if key not in accepted_keys:
            return False

    return True


def has_required_keys(data, required_keys):
    """
    Returns if the data doesn't contain any key that is present in required_keys
    :param data: The object to be verified.
    :param required_keys: The list of keys that must be present
    :return: boolean: Result of the verification
    """
    if data is None:
        return False
    data_keys = data.keys()
    for key in required_keys:
        if key not in data_keys or is_none_or_empty(data[key]):
            return False

    return True


def is_none_or_empty(data):
    if data is None:
        return True
    elif type(data) == str and data.strip() == '':
        return True
    elif (type(data) == list or type(data) == dict) and not data:
        return True
    else:
        return False


def is_valid_email(email):
    return re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)