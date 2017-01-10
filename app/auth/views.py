from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from . import auth
from .forms import RegForm, LogForm
from .. import db
from ..models import User


@auth.route("/register", methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        user = User(form.email.data, form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно', 'alert alert-success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LogForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.authenticate(form.password.data):
            login_user(user)
            flash('Вход произошел успешно', 'alert alert-success')
            return redirect(url_for('main.list'))
        flash('Неверная эл. почта или пароль', 'alert alert-warning')
    return render_template('login.html', form=form)


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'alert alert-warning')
    return redirect(url_for('main.home'))
