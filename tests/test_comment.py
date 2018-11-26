from app.models import User, Comments
from app import db

def setUp(self):
  self.user_James = User('James', password='potato', email='james@ms.com')
  
  self.new_comment = Comments(pitch_id=12345, pitch_title='Comments on pitches', pitch_comment='This pitch has promise', user=self.user_James)

def tearDown(self):
  Review.query.delete()
  User.query.delete()

def test_check_instance_variables(self):
  self.assertEquals(self.new_comment.pitch_id, 12345)

  self.assertEquals(self.new_comment.pitch_title, 'Comments on pitches')

  self.assertEquals(self.new_comment.pitch_comment, 'This pitch has promise')

  self.assertEquals(self.new_comment.user, self.user_James)

def test_save_comment(self):
  self.new_comment.save_comment()
  self.assertTrue(len(Comments.query.all())>0)

def test_get_comment_by_id(self):
  self.new_comment.save_comment()
  got_comments = Comments.get_comments(12345)
  self.assertTrue(len(got_comments) == 1)