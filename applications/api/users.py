import json
from datetime import datetime, timedelta
from applications.models.models import User
from flask import ( request, Blueprint )
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt
from applications import db
from util.utilities import ( has_required_keys, has_allowed_keys, is_valid_email)
from util.response import get_error_response, get_client_error_response, get_server_error_response, get_availability_response, get_success_response


user_blueprint = Blueprint('user', __name__, url_prefix='/users')


@user_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create():
    try:
        claims = get_jwt()
        if claims["role"] == "admin":
            data = request.json
            required_keys = ['first_name', 'last_name', 'email']
            if not has_required_keys(data, required_keys):
                return get_client_error_response(message='Invalid request. Fields required ({})'.format(required_keys), error_code=422)
            if not is_valid_email(data.get('email')):
                return get_client_error_response(message='Invalid email ({})'.format(data.get('email')))
            exists = User.find_by_email(data.get('email'))
            if exists is not None :
                return {'message': 'Email {} already exists'. format(data.get('email'))}
            password = User.generate_hash('password')
            new_user = User(
                email = data.get('email'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                password = password,
                user_type = 2
            )
            new_user.save_to_db()
            return get_success_response(message='User has been created', response_code=201)
        else:
            return get_client_error_response(message='Unauthorize', error_code=401)
    except Exception as e:
        print(e)
        return get_server_error_response()   
        
        





