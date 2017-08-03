from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,  login_required

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from.import db

from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'login'

class Permission(): # Permission=权限
    FOLLOW=0x01
    COMMENT=0x02
    WRITE_ARTICLES=0x04
    MODERATE_COMMENTS=0x08
    ADMINISTER=0x80

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    #只有一个角色的default设置为True,其他的设置为Flase.用户注册的时候，其角色会被设置为默认角色
    permissions=db.Column(db.Integer)
    #permissions其值是一个整数，表示位标志。各种操作都对应一个位位置，能执行某种操作的角色，其位会设为1
    user=db.relationship('user',backref='role',lazy='dynamic')

    #_____角色的权限_____97


    @staticmethod
    def insert_roled():
        roles={
            'User':(Permission.FOLLOW,Permission.COMMENT,Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW,Permission.COMMENT,Permission.WRITE_ARTICLES,Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)

        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                r = role
            #_____???
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            #_____???
            db.session.add(role)
    db.session.commit()


    #____第九章权限的常量____98

class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 16)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.Integer,unique=True,index=True)

    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    #.修改User模型，支持永和登陆--p82

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    confirmed=db.Column(db.Boolean,default=False)
    def generate_confirmation_token(self,expiration=3600):
        s =Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s =Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    #用户确认账户

    def __repr__(self):
        return '<User {0}>'.format(self.username)
    #增加密码散列

    #________第九章内容（定义默认的用户角色page99）______________
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email==current_app.config['FLASK_ADMIN']:
                self.role=Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()

 #____检查用户是否有指定的权限__100
    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.cam(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False
login_manager.anonymous_user=AnonymousUser

    #________第九章内容结束________________________________

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#回调函数

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


if __name__ == '__main__':
    db.create_all()
    if User.query.filter_by(username='john').first() is None:
        User.register('john', 'cat')
    app.run(debug=True)




