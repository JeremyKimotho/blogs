from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager



@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):

ACCESS = {
  'user': 0,
  'admin': 1
}

  __tablename__='users'

  id = db.Column(db.Integer(), primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255))
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

  def is_admin(self):
    return self.access == ACCESS['admin']
    
  def allowed(self, access_level):
    return self.access >= access_level

  def init_db():
  if User.query.all().count() == 0:
    master = User(username='master', password='master', first_name='Jeremy', surname='Kimotho', email='projectsjeremy1000@gmail.com', access=ACCESS['admin'])
    save_user(master)

  def __repr__(self):
    return f'User {self.username}'

class Comments(db.Model):
  __tablename__='comments'

  id = db.Column(db.Integer(), primary_key = True)
  comment = db.Column(db.String)
  user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  post = db.Column(db.Integer, db.ForeignKey('posts.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_comments(cls, id):
    comments = Comments.query.filter_by(post_id=id).all()
    return comments

class Post(db.Model):
  __tablename__='posts'

  id = db.Column(db.Integer(), primary_key = True)
  title = db.Column(db.String(255))
  body = db.Column(db.String())
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
