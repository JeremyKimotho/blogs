import unittest
from app.models import User

class UserModelTest(unittest.TestCase):

  def setUp(self):
    self.new_user=User(password='banana')

  def test_password_setter(self):
    self.assertTrue(self.new_user.pass_secure is not None)

  def test_no_access_password(self):
    with self.assertRaises(AttributeError):
      self.new_user.password

  def test_password_verfication(self):
    self.assertTrue(self.new_user.verify_password('banana'))

  def test_save_user(self):
    self.new_user.save_user()
    self.assertTrue(len(User.query.all())>0)