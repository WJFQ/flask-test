from flask import render_template,session,redirect,url_for,request,flash
from flask_login import login_user,logout_user,login_required,current_user
from.import auth
from..import db
from..models import User
from ..email import send_email
from.forms import  LoginForm, RegistrationForm
'''
url_for():FLASK提供的辅助函数，他可以使用程序的URL映射中保存的信息生成URL PAGE 29
User.query.filter_by
request.args.get
redirect
validate
'''
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth'and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('unconfirmed')
def unconfirmed():
    if current_user.is_anonumous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
#处理程序中过滤未确认的账户--p94

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    #LoginForm()在隔壁的forms.py
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('index') or url_for('main.index'))
        flash('账户或密码格式不对')
    return render_template('auth/login.html',form=form)
#用户登入--p84

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登陆')
    return redirect(url_for('main.index'))
    #用户登出--p86

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user =User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        flash('你现在可以登陆')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
    #RegistrationForm() 在隔壁的forms.py
    #用户注册路由--p90

@auth.route('/comfirm/<token>')
@login_required
def confirm(token):
    if current_user.confirm:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经确认了你的账户')
    else:
        flash('确认链接已经失效或无法使用')
    return redirect(url_for('main.index'))
#确认用户的账户--p93

@auth.route('/confirm')
@login_required
def resend_confirmeation():
    token=current_user.generate_confirmation_token()
    #current_user 激活user的实例
    send_email(current_user.email,'确认你的账号','auth/email/comfirm',user=current_user,token=token)
                                                        #'auth/email/comfirm'是文件夹地址吗？
    flash('一个新的确认邮件已经发送给你')
    return redirect(url_for('main.index'))
#重新发送确认邮件--p94
#_______________________________________________