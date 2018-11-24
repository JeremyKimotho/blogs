from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import RegistrationForm, LoginForm
from .. import db
from ..email import welcome_mail_message


@auth.route('/register', methods=['GET', 'POST'])
def register():
  User.init_db()
  form = RegistrationForm()

  if form.validate_on_submit():
    user = User(email=form.email.data, username=form.username.data, password=form.password.data, first_name=form.fname.data, surname=form.lname.data)

    User.save_user(user)

    welcome_mail_message('Welcome to Jlogs', 'email/welcome_email', user.email, user=user)
    return redirect(url_for('auth.login'))
    title='New Jlogs Account'

  return render_template('auth/register.html', registration_form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  User.init_db()
  login_form = LoginForm()
  if login_form.validate_on_submit():
    user = User.query.filter_by(username=login_form.username.data).first()
    session['username']=login_form.username.data
    if user is not None and user.verify_password(login_form.password.data):
      login_user(user, login_form.remember.data)
      return redirect(request.args.get('next') or url_for('main.index'))

    flash('Invalid Username or Password')

  title = 'Jlogs Login'
  return render_template('auth/login.html', login_form = login_form, title = title)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

