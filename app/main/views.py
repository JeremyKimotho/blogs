from flask import render_template, request, redirect, url_for, abort, flash, session
from . import main
from ..models import User, Post, Comments
from ..date_pipe import date_calc
from flask_login import login_required, current_user
from .. import db
from datetime import datetime
from functools import wraps

def requires_admin(access_level):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if not session.get('username'):
        return redirect(url_for('auth.login'))
      user = User.find_by_username(session['username'])
      if not user.allowed(access_level):
        return redirect(url_for('main.index', message='You do not have the required permissions to access that'))
      return f(*args, **kwargs)
    return decorated_function
  return decorator

@main.route('/')
@login_required
def index():
  title='Welcome to Jeiter'
  time=datetime.now()
  return render_template('index.html', title=title, time=time)

@main.route('/profile/user/<uname>/')
def profile_user(id, uname):
  user = User.query.filter_by(username = uname)
  memberFor=date_calc(User.joined)
  return render_template('profile/profile.html', memberFor=memberFor)