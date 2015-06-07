# !/usr/bin/dev python
# -*- coding:utf-8 -*-

from flask import render_template, current_app, request, \
                            redirect, url_for, flash

from flask.ext.login import login_user, logout_user, login_required
from ..models import User, registerUser 
from . import auth
from .forms import LoginForm, RegisterForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not \
            current_app.config['TESTING'] and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.')
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('talks.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('talks.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """ Register a new user. """
    form = RegisterForm()
    msg = ''

    if form.validate_on_submit():
        username = form.username.data
        password1 = form.password.data
        password2 = form.password1.data
        email = form.email.data
        reason = form.reason.data

        if password1 != password2:
            msg = u'两次输入的密码不一致!'
        elif registerUser.query.filter_by(username=username).first():
            msg = u'用户名已存在, 请使用其他用户名!'
        elif registerUser.query.filter_by(email=email).first():
            msg = u'该邮箱已被使用, 请使用其他邮箱!'
        
        if msg:
            flash(msg)
            return render_template('auth/register.html', form=form)

        registeruser = registerUser(\
            username=username, password=password1,email=email,reason=reason)
        db.session.add(registeruser)
        db.session.commit()

        flash(u'用户申请成功, 请等待管理员审核')
        return redirect(url_for('talks/index.html'))
    return render_template('auth/register.html', form=form)


@auth.route('/user_aproval')
def aproval():
    """ Get and Show users list which are not granted. """
    return 'hey'
