import unittest
from app.models import User
from dataetime import datetime

class UserModelTest(unittest.TestCase):

  def setUp(self):
    self.new_user=User(1, 'jeremy', 'j@j.com', datetime.now(), 'j', 'j', password='banana', access=1)

  def tearDown(self):
    User.query.delete()

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

  def test_find_user(self):
    self.new_user.save_user()
    found_user = User.find_by_username('jeremy')
    self.assertTrue(len(found_user.username) == 'jeremy')

  def test_access_level(self):
    self.new_user.save_user()
    user = User.query.all().first()
    user_admin = self.user.is_admin()
    self.assertTrue(len(user_admin) == True)

  def test_is_user_allowed(self):
    self.new_user.save_user()
    user = User.query.all().first()
    user_access = self.user.allowed(user, 0)
    self.assertTrue(len(user_access) == True)

  def test_master(self):
    master = User.init_db()
    all_users = User.query.all()
    self.assertTrue(len(all_users) == 1)

  