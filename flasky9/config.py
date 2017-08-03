import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PERFIX = '[Flasky]'
    FLASK_MAIL_SENDER='Flasky Admin <597898719@qq.com>'
    #邮箱

    FLASK_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG =True
    MAIL_SERVER = 'smtp.163.com'
    #邮箱服务器

    MAIL_PORT =587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('597898719@qq.com')
    MAIL_PASSWORD=os.environ.get('A62660313')

    SQLALCHEMY_DATABASE_URI= os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')
    #程序使用数据库，并且获得了Flask-SQLAlchemy提供的所有功能

class TestingConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data.sqlite')

config ={
        'development': DevelopmentConfig,
        'testing':TestingConfig,
        'production':ProductionConfig,
        'default':DevelopmentConfig

    }
#_______________________________________________