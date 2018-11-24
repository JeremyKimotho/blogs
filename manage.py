from app import create_app, db
from app.models import User, Comments, Post
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('development')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
  import unittest
  tests = unittest.TestLoader().discover('tests')

@manager.shell
def make_shell_context():
  return dict(app=app, db=db, Post=Post, User=User, Comments=Comments)

if __name__=='__main__':
  manager.run()