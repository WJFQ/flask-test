from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

from flask_login import LoginManager
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
#初始化flask login

bootstrap = Bootstrap()
mail =Mail()
moment =Moment()
db =SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    #初始化flask login
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    #附加路由 (注册蓝本)
    from.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')


    #定义错误页面

    return app

#_______________________________________________