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
  return render_template('index.html', title=title)

@main.route('/profile/user/<uname>/<id>')
def profile_user(id, uname):
  user = User.query.filter_by(username = uname).first()
  memberFor=date_calc(user.joined)
  return render_template('profile/profile.html', memberFor=memberFor)

@main.route('/profile/admin/<uname>/<id>')
def profile_admin(id, uname):
  nō_users=User.query.all()
  nō_posts=Post.query.all()
  return render_template('profile/admin.html', users=nō_users, posts=nō_posts)

@main.route('/writing-posts', methods=['GET', 'POST'])
@login_required
def write_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, body=form.body.data)

    Post.save_post(post)
    return redirect(url_for('main.index'))

  title='New Blog Post'
  return render_template('new_post.html', post=form, title=title)
