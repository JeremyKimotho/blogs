import unittest
from app.models import Post
from datetime import datetime

class PostTest(unittest.TestCase):

  def setUp(self):
    
    self.new_post = Post(1, 'title', 'body', datetime.now())

  def test_instance(self):
    self.assertTrue(isinstance(self.new_post, Post))

  def test_save_post(self):
    self.new_post.save_post()
    self.assertTrue(len(Post.query.all())>0)

  def test_get_posts(self):
    self.new_post.save_post()
    got_posts = Post.get_specific_post(1)
    self.assertTrue(len(got_posts) == 1)

  def test_get_all_posts(self):
    self.new_post.save_pitch()
    got_posts = Post.get_posts()
    self.assertTrue(len(got_posts) == 1)

  def test_get_post_comments(self):
    self.new_post.save_post()
    got_post_comments = Post.get_comments()
    self.assertTrue(len(got_post_comments)>=0)

  def test_delete_post(self):
    self.new_post.save_post()
    self.new_post.delete_post()
    self.assertTrue(len(Post.query.all()) == 0)

  def test_default_posts(self):
    posts = Post.default_posts()
    all_posts = Post.query.all()
    self.assertTrue(len(all_posts) == 8)

