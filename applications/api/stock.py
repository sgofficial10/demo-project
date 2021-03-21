import json
from datetime import datetime, timedelta
from applications.models.models import User
from flask import ( request, Blueprint )
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt
from applications import db
from util.utilities import ( has_required_keys, has_allowed_keys)
from util.response import get_error_response, get_client_error_response, get_server_error_response, get_availability_response, get_success_response
from yahoo_finance import Share



stock_blueprint = Blueprint('stock', __name__, url_prefix='/stock')


@stock_blueprint.route('/get_share_price', methods=['POST'])
def share_price():
    try:
        data = request.json
        required_keys = ['share_name']
        if not has_required_keys(data, required_keys):
            return get_client_error_response(message='Invalid request. Fields required ({})'.format(required_keys), error_code=422)
        yahoo = Share(data.get('share_name'))
        price = yahoo.get_price()
        print(price)
        # resp = {}
        # resp['share_name'] = data.get('share_name')
        # resp['price']  = price
        # return get_success_response(message='Price details', data=resp)
    except Exception as e:
        print(e)
        return get_server_error_response()
