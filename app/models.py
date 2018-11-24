from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):
  __tablename__='users'

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255))
  first_name = db.Column(db.String(255))
  surname = db.Column(db.String(255))
  pass_secure = db.Column(db.String(255))

  comments = db.relationship('Comments', backref='comments', lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('You do not have the permissions to access this')

  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.pass_secure, password)

  def save_user(self):
    db.session.add(self)
    db.session.commit()

  def __repr__(self):
    return f'User {self.username}'

class Comments(db.Model):
  __tablename__='comments'

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  post = db.Column(db.Integer, db.ForeignKey('post.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_comments(cls, id):
    comments = Comments.query.filter_by(post_id=id).all()
    return comments

class Post(db.Model):
  __tablename__='posts'

  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))
  body = db.Column(db.String)
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  
  comments = db.relationship('Comments', backref='comments1', lazy='dynamic')

  def save_post(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_posts(cls, id):
    posts = Post.query.all()
    return posts

  def get_comments(self):
    post = Post.query.filter_by(id = self.id).first()
    comments = Comments.query.filter_by(post=post.id)
    return comments

  
    
