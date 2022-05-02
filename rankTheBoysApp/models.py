from datetime import datetime
from rankTheBoysApp import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    pools = db.relationship('Pool', secondary='userpools')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}'"

class Pool(db.Model):
    __tablename__ = 'pools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', secondary='userpools')

    def __repr__(self):
        return f"Pool: {self.name}"

class UserPool(db.Model):
    __tablename__ = 'userpools'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pool_id = db.Column(db.Integer, db.ForeignKey('pools.id'))
    rating = db.Column(db.Float)

    user = db.relationship(User, backref=backref('userpools', cascade="all, delete-orphan"))
    pool = db.relationship(Pool, backref=backref('userpools', cascade="all, delete-orphan"))

    def __repr__(self):
        return f"UserPool: {self.id}, PoolId: {self.pool_id}, UserID: {self.user_id}"

    

