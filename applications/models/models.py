from applications import db
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy_serializer import SerializerMixin



class TimeStamp(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)


user_roles = db.Table('user_roles', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(TimeStamp, db.Model):
    __tablename__ = 'user'


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.Text, unique=False, nullable=False)
    user_type = db.Column(db.SmallInteger, default=1)
    access_token = db.Column(db.Text, nullable=True)


    roles = db.relationship("Role", secondary="user_roles", back_populates="users")



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'id': self.id,
            'access_token': self.access_token,
            'user_type': self.user_type
        }


    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)



    def __repr__(self):
        return '<User %r>' % (self.first_name)


class Role(TimeStamp, db.Model, SerializerMixin):
    __tablename__ = 'role'


    serialize_only = ('role_name', 'description', 'id', 'is_active')

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.SmallInteger, default=1)

    users = db.relationship("User", secondary="user_roles", back_populates="roles")


    def __repr__(self):
        return '<Role %r>' % (self.role_name)


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def to_json(self):
        return {
            'role_name': self.role_name,
            'description': self.description,
            'id': self.id,
            'is_active': self.is_active
        }




