import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)



    db.init_app(app)
    with app.app_context():
        # Register blueprints
        from applications.api.users import user_blueprint
        from applications.api.role import role_blueprint
        from applications.api.auth import auth_blueprint
        from applications.api.stock import stock_blueprint
        app.register_blueprint(user_blueprint)
        app.register_blueprint(role_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(stock_blueprint)
        return app