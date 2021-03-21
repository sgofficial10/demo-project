import json
from datetime import datetime, timedelta
from applications.models.models import Role, User
from flask import ( request, Blueprint )
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt
from applications import db
from util.utilities import ( has_required_keys, has_allowed_keys, is_valid_email)
from util.response import get_error_response, get_client_error_response, get_server_error_response, get_availability_response, get_success_response




role_blueprint = Blueprint('role', __name__, url_prefix='/role')


@role_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create():
    try: 
        claims = get_jwt()
        if claims["role"] == "admin":
            data = request.json
            required_keys = ['role_name', 'description']
            if not has_required_keys(data, required_keys):
                return get_client_error_response(message='Invalid request. Fields required ({})'.format(required_keys), error_code=422)
            new_role = Role(
                role_name = data.get('role_name'),
                description = data.get('description')
            )
            new_role.save_to_db()
            return get_success_response(message='Role has been created', response_code=201)
        else:
            return get_client_error_response(message='Unauthorize', error_code=401)
    except Exception as e:
        print(e)
        return get_server_error_response()   

@role_blueprint.route('/list/<int:page>', methods=['GET'], defaults={"page": 1})
@jwt_required()
def list(page=1):
    try: 
        claims = get_jwt()
        if claims["role"] == "admin":
            items = []
            per_page = 2
            role_list = Role.query.all()
            for single_role in role_list:
                items.append(single_role.to_json())
            return get_success_response(message='Role list has been fetched.', data=items)
        else:
            return get_client_error_response(message='Unauthorize', error_code=401)
    except Exception as e:
        print(e)
        return get_server_error_response()   




@role_blueprint.route('/assign_role', methods=['POST'])
@jwt_required()
def assignRole():
    try:
        claims = get_jwt()
        if claims["role"] == "admin":
            data = request.json
            required_keys = ['user_id', 'role_id']
            if not has_required_keys(data, required_keys):
                return get_client_error_response(message='Invalid request. Fields required ({})'.format(required_keys), error_code=422)
            user_details = User.find_by_id(data.get('user_id'))
            role_details = Role.find_by_id(data.get('user_id'))
            if user_details is None or role_details is None:
                return get_error_response(message='Invalid user details')  
            user_details.roles.append(role_details)
            db.session.add(user_details)
            db.session.commit()
            return get_success_response(message='Role has been assigned', response_code=200)
        else:
            return get_client_error_response(message='Unauthorize', error_code=401)
    except Exception as e:
        print(e)
        return get_server_error_response()   


@role_blueprint.route('/remove_role', methods=['POST'])
@jwt_required()
def removeRole():
    try:
        claims = get_jwt()
        if claims["role"] == "admin":
            data = request.json
            required_keys = ['user_id', 'role_id']
            if not has_required_keys(data, required_keys):
                return get_client_error_response(message='Invalid request. Fields required ({})'.format(required_keys), error_code=422)
            user_details = User.find_by_id(data.get('user_id'))
            role_details = Role.find_by_id(data.get('user_id'))
            if user_details is None or role_details is None:
                return get_error_response(message='Invalid user details')  
            user_details.roles.remove(role_details)
            db.session.commit()
            return get_success_response(message='Role has been assigned', response_code=200)
        else:
            return get_client_error_response(message='Unauthorize', error_code=401)
    except Exception as e:
        print(e)
        return get_server_error_response()







