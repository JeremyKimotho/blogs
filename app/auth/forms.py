from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo
from ..models import User
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
  fname = StringField('Your first name', validators=[Required()])
  lname = StringField('Your last name', validators=[Required()])
  email = StringField('Your email address', validators=[Required(), Email()])
  username = StringField('Enter a username', validators=[Required()])
  password = PasswordField('Password', validators=[Required(), EqualTo('password_confirm', message='Passwords must match')])
  password_confirm = PasswordField('Confirm password', validators=[Required()])
  submit = SubmitField('Sign Up')

  def validate_email(self, data_field):
    if User.query.filter_by(email = data_field.data).first():
      raise ValidationError('An account with that email already exists')
    
  def validate_username(self, data_field):
    if User.query.filter_by(username = data_field.data).first():
      raise ValidationError('That username is taken')

  def init_db():
    if User.query.all().count() == 0:
      master = User(username='master', password='master', first_name='Jeremy', surname='Kimotho', email='projectsjeremy1000@gmail.com', access=ACCESS['admin'])
      save_user(master)

class LoginForm(FlaskForm):
  username = StringField('Your Username', validators=[Required()])
  password = PasswordField('Password', validators=[Required()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')