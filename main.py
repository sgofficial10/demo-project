import json
from applications import create_app, db
from applications.models import models
from applications.models.models import User
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



app = create_app()
with open('configurations/db_config.json', 'r') as f:
    conf = json.loads(f.read())
    mysql_conf = conf['MYSQL']
    # mongo_conf = conf['MONGO']

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}".format(**mysql_conf)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with open('configurations/security_config.json', 'r') as s:
    conf = json.loads(s.read())
    app.config['JWT_SECRET_KEY'] = conf['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = conf['TOKEN_VALIDITY_DURATION_SECONDS']
    app.config['JWT_BLACKLIST_ENABLED'] = False
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']


jwt = JWTManager(app)

migrate = Migrate(app, db)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity






if __name__ == '__main__':
    app.run()