from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class PostForm(FlaskForm):
  title=StringField('Blog Title')
  body=TextAreaField('Write Away')
  submit=SubmitField('Submit')

class CommentForm(FlaskForm):
  comment=TextAreaField('Your comment:')
  submit=SubmitField('Post')