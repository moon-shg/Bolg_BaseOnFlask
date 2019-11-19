from . import auth
from flask import render_template, request, redirect, url_for, flash
from .forms import LoginForm
from ..models import User
from flask_login import login_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main.index')
                flash('欢迎回来！')
            return redirect(next)
        flash('邮箱或密码错误！')
    return render_template('auth/login.html', form=form)
