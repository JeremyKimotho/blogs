from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

ACCESS = {
  'user': 0,
  'admin': 1
}

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):

  __tablename__='users'

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255))
  joined=db.Column(db.DateTime,default=datetime.now)
  first_name = db.Column(db.String(255))
  surname = db.Column(db.String(255))
  pass_secure = db.Column(db.String(255))
  access=db.Column(db.String(255), default=ACCESS['user'])

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

  def find_by_username(cls, username):
    user = User.query.filter_by(username=username).first()
    return user

  def is_admin(self):
    return self.access == ACCESS['admin']
    
  def allowed(self, access_level):
    return self.access >= access_level

  def init_db():
    if User.query.count() == 0:
      master = User(username='master', password='master', first_name='Jeremy', surname='Kimotho', email='projectsjeremy1000@gmail.com', access=ACCESS['admin'])
      
      db.session.add(master)
      db.session.commit()

  def __repr__(self):
    return f'User {self.username}'

class Comments(db.Model):
  __tablename__='comments'

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  posted = db.Column(db.DateTime,default=datetime.now)
  post = db.Column(db.Integer, db.ForeignKey('posts.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_comments(cls, id):
    comments = Comments.query.filter_by(posted=id).all()
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

  def delete_post(self):
    db.session.delete(self)
    db.session.commit()

  def get_specific_post(id):
    post = Post.query.filter_by(id=id).first()
    return post

  @classmethod
  def get_posts(cls):
    posts = Post.query.all()
    return posts

  def get_comments(self):
    post = Post.query.filter_by(id = self.id).first()
    comments = Comments.query.filter_by(post=post.id)
    return comments
