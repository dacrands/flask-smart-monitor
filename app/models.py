from app import app, db
from app import login
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, unique=False, default=False)
    latitude = db.Column(db.String(64), default=0.0)
    longitude = db.Column(db.String(64), default=0.0)
    stocks = db.relationship('Stock', backref='author', lazy='dynamic')
    todos = db.relationship('Todo', backref='author', lazy='dynamic')
    embeds = db.relationship('Embed', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_location(self, lat, lon):
        (self.latitude, self.longitude) = (lat, lon)

    def get_email_token(self, expires_in=600):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def set_verify(self, authBool):
        self.is_verified = authBool

    @staticmethod
    def verify_email_token(token):
        try:
            jwt_id = jwt.decode(token, app.config['SECRET_KEY'],
                                algorithms=['HS256'])['verify_email']
        except:
            return None
        return jwt_id


class Stock (db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(20), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.symbol)


class Todo (db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    todo = db.Column(db.String(256), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Todo {}>'.format(self.todo)


class Embed(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    embed = db.Column(db.String(40), index=True)
    name = db.Column(db.String(40), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Embed {}>'.format(self.embed)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
