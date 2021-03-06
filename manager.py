import os
import sys
from flask_migrate import Migrate, MigrateCommand, upgrade #载入migrate扩展
from app import db
from flask_script import Manager, Shell
from run import app
from app.models import User, Role

migrate = Migrate(app, db)  #注册migrate到flask
manager = Manager(app)

manager.add_command('db', MigrateCommand) #在终端环境下添加一个db命令

COV = None
if os.environ.get('COVERAGE'):
    import coverage
    COV=coverage.coverage(branch=True,include='app/*')
    COV.start()
    print('Start measuring code coverage')
    
@manager.command
def test(coverage=False):
    """Run the unittests"""
    if coverage and not os.environ.get('COVERAGE'):
        os.environ['COVERAGE']='1'
        # 重启脚本，设置了FLASK_COVERAGE，启动覆盖检测
        print('Reset')
        # .executable:python可执行文件路径
        # 执行可执行文件
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

@manager.command
def init_data():
    db.create_all()
    Role.insert_roles()
    admin_role = Role.query.filter_by(name='Administrator').first()
    user_role = Role.query.filter_by(name='User').first()
    moderate_role = Role.query.filter_by(name='Moderate').first()
    u1 = User(role=user_role, confirmed=True, email='user1@test.com',
                  password='123', user_name='user1')
    u2 = User(role=moderate_role, confirmed=True, email='user2@test.com',
              password='123', user_name='user2')
    u3 = User(role=admin_role, confirmed=True, email='user3@test.com',
              password='123', user_name='user3')
    db.session.add_all([u1, u2, u3])
    db.session.commit()

@manager.command
def deploy():
    """安装升级"""
    # 数据库迁移到最新版本
    upgrade()
    
    # 添加3中角色
    Role.insert_roles()
    
    # 每个用户都关注自己
    User.add_self_follows()

if __name__ == '__main__':
    manager.run()
