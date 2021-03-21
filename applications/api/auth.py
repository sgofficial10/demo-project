import json
from datetime import datetime, timedelta
from applications.models.models import Role, User
import bcrypt
from flask import ( request, Blueprint )
from flask_jwt_extended import create_access_token, jwt_required
from applications import db
from util.utilities import ( has_required_keys, has_allowed_keys, is_valid_email)
from util.response import get_error_response, get_client_error_response, get_server_error_response, get_availability_response, get_success_response




auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')





@auth_blueprint.route('/admin_login', methods=['POST'])
def login():
    try: 
        data = request.json
        required_keys = ['email', 'password']
        if not has_required_keys(data, required_keys):
            return get_client_error_response(message='Invalid request. Fields required ({})'.format(required_keys), error_code=422)
        if not is_valid_email(data.get('email')):
            return get_client_error_response(message='Invalid email ({})'.format(data.get('email')))
        admin_user_details = User.query.filter_by(email=data.get('email'), user_type=1).first()
        if admin_user_details is None:
            return get_client_error_response(message='Invalid credentials!', error_code=401)
        if admin_user_details.deleted_at is not None:
            return get_client_error_response(message='Invalid credentials!', error_code=401)
        status = User.verify_hash(data.get('password'), admin_user_details.password)
        if status == False:
            return get_client_error_response(message='Invalid credentials!', error_code=401)
        additional_claims = {"role": "admin"}
        access_token = create_access_token(admin_user_details, additional_claims=additional_claims)
        admin_user_details.access_token = access_token
        db.session.commit()
        return get_success_response(message='Login successful', data=admin_user_details.to_json())
    except Exception as e:
        print(e)
        return get_server_error_response()
