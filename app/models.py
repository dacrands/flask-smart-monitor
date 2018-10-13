from app import app, db
from app import login
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, unique=False, default=False)
    stocks = db.relationship('Stock', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
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
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.symbol)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))