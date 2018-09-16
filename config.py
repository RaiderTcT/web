# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:62300313@localhost:3306/sql_hello?charset=utf8mb4"
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# SECRET_KEY = 'role user test'
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
import os
from user_setting import *


class Config:
    SECRET_KEY = os.environ.get('SECRET_KKEY') or 'you never guss'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.qq.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or qqmail_user
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or qqmail_passwd
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '2276777056@qq.com'
    FLASK_ADMIN = os.environ.get("FLASK_ADMIN") or 'jianliangwu1171@gmail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


#   开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    DBNAME = 'sql_hello'
    URL = f'mysql+pymysql://{root}:{passwd}@localhost:3306/{DBNAME}'
    SQLALCHEMY_DATABASE_URI = URL


class TestingConfig(Config):
    TESTING = True
    DBNAME = 'sql_test'
    URL = f'mysql+pymysql://{root}:{passwd}@localhost:3306/{DBNAME}'
    SQLALCHEMY_DATABASE_URI = URL


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig
}