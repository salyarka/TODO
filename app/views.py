from app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from app.forms import RegForm, TodoForm, LogForm
from app.models import User
from flask_login import login_user, login_required, logout_user


@app.route("/")
def home():
  return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def reg():
  form = RegForm()

	# if form.validate... переделать

  if form.validate_username(form.username.data):					
    flash('Пользователь с таким именем уже существует.')
    return render_template('register.html', form=form)   

  if form.validate_email(form.email.data):
    flash('Такой email уже зарегистрирован.')
    return render_template('register.html', form=form)   

  if form.validate_on_submit():
    user = User(form.email.data, form.username.data, form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Регистрация прошла успешно')
    return redirect(url_for('home'))
  return render_template('register.html', form=form)   	


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LogForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.authenticate(form.password.data):
      login_user(user)
      flash('Вход произошел успешно')
      return redirect(url_for('todo'))
    flash('Неверная эл. почта или пароль')
  return render_template('login.html', form=form)  


@app.route("/logout", methods=['GET', 'POST'])
def logout():
  logout_user()
  flash('Вы вышли из аккаунта')
  return redirect(url_for('home'))



@app.route ("/todo")
@login_required
def todo():	
  form = TodoForm()
  return render_template('todo.html', form=form)
