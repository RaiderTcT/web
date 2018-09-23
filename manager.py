import os
from flask_migrate import Migrate, MigrateCommand #载入migrate扩展
from app import db
from flask_script import Manager, Shell
from run import app

migrate = Migrate(app, db)  #注册migrate到flask
manager = Manager(app)

manager.add_command('db', MigrateCommand) #在终端环境下添加一个db命令

COV = None
if os.environ.get('COVERAGE'):
    import coverage
    COV=coverage.coverage(branch=True,include='*')
    COV.start()
    print('Start measuring code coverage')
    
@manager.command
def test(coverage=False):
    """Run the unittests"""
    if coverage and not os.environ.get('COVERAGE'):
        import sys
        os.environ['COVERAGE']='1'
        os.execvp(sys.executable,[sys.executable]+sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage:')
        COV.report()
        COV.html_report(directory='COV-html')
        COV.erase()

if __name__ == '__main__':
    manager.run()