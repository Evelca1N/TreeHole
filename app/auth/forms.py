# !/usr/bin/dev python
# -*- coding:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    email = StringField(u'注册邮箱', \
                            validators=[Required(), Length(1,64),Email()])
    username = StringField(u'用户名', \
                            validators=[Required(), Length(1,64)])
    password = PasswordField(u'密码', \
                            validators=[Required(), Length(1, 16)])
    password1 = PasswordField(u'确认密码', \
                            validators=[Required(), Length(1, 16)])
    reason = StringField(u'请简要阐述注册理由', \
                            validators=[Length(1,128)])
    submit = SubmitField(u'注册')
