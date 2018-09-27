import os
from app import create_app, db
from app.models import User, Role,Post, Follow, Permission
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
#app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
app = create_app('default')
migrate = Migrate(app, db)
    
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post, Follow=Follow, Permission=Permission)

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)
    