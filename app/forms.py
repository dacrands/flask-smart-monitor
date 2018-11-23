from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In \u203A')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register \u203A')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DeleteUserForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Delete account')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset \u203A')

class NewPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset \u203A')

class StockForm(FlaskForm):
    symbol = StringField('Enter ticker symbol: ', validators=[DataRequired()])
    submitStock = SubmitField('Add stock \u203A')

class EmbedForm(FlaskForm):
    embed = StringField('Enter embed: ', validators=[DataRequired()])
    name = StringField('Give it a name: ', validators=[DataRequired()])
    submitEmbed = SubmitField('Add embed \u203A')

class TodoForm(FlaskForm):
    todo = StringField('Enter todo: ', validators=[DataRequired(), Length(
                                                        min=1, 
                                                        max=250, 
                                                        message="Todo must be between %(min)s and %(max)s \
                                                        characters in length")])
    submitTodo = SubmitField('Add todo \u203A')


class LocationForm(FlaskForm):
    lat = FloatField('Latitude: ', validators=[DataRequired()])
    lon = FloatField('Longitude: ', validators=[DataRequired()])
    submitLoc = SubmitField('Set location \u203A')