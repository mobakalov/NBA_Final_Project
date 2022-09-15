from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from app.models import User


class PlayerForm(FlaskForm):
    player= StringField('Player Name',validators = [DataRequired()])
    submit = SubmitField('Search')

class CompareForm(FlaskForm):
    season1 = StringField('First Player\'s Season',validators = [DataRequired()])
    player1= StringField('First Player Name',validators = [DataRequired()])
    season2 = StringField('Second Player\'s Season',validators = [DataRequired()])
    player2 = StringField('Second Player Name',validators = [DataRequired()])
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators = [DataRequired(), EqualTo('password', message = 'Passwords must match')])
    submit = SubmitField('Register')
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
        
        if same_email_user:
            raise ValidationError('This email is already being used, try again.')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message = 'Passwords must match')])
    submit = SubmitField('Update')