'''
此三个都在  page12
request：请求对象，封装了客户端发出的HTTP请求中的内容
session：用户对话，存储请求之间需要记住的字典
current_app：激活当前程序的实例

StringField,
PasswordField.          是WTForm中支持的HTML标准字段 page 35
BooleanField,
SubmitField
'''
from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
#这里是WTFORM的验证函数 PAGE 35
from ..models import User


class LoginForm(Form):
    email=StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('密码',validators=[Required()])
    remember_me=BooleanField('记住密码')
    submit =SubmitField('登陆')
    '''登陆界面 分别有 邮箱 密码 记住密码  登陆 四个按键'''

class RegistrationForm(Form):   #创建账户密码
    email=StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    username =StringField('用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
    #账号的格式
    password =PasswordField('密码',validators=[Required(),EqualTo('password2',message='Password must match')])
    password2=PasswordField('确认密码',validators=[Required()])
    submit =SubmitField('创建')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('邮箱已经存在')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValueError('用户名已经被使用')
'''
PAGE 54
.first()数据库的查询执行函数返回查询的第一个结果。如果没有，则返回none
是否可以理解为：用户输入的邮箱 用户名 会存入 field.data中
并且在数据库中用.first() 执行查询
'''
#未完
#_______________________________________________