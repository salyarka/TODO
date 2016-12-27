from app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from app.forms import RegForm, TodoForm, LogForm, TodoListForm
from app.models import User, Todo, TodoList
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


@app.route("/list/", methods=['GET', 'POST'])
@app.route("/list/<id>", methods=['GET', 'POST'])
def list(id=None):
    form = TodoListForm()
    lists = TodoList.query.order_by('title')
    if form.validate_on_submit():
        todo_list = TodoList(form.title.data)
        db.session.add(todo_list)
        db.session.commit()
        flash('Список добавлен')
        return redirect(url_for('list'))
    return render_template('todolist.html', lists=lists, form=form)


@app.route("/todo", methods=['GET', 'POST'])
@login_required
def todo():
    form = TodoForm()
    todos = Todo.query.order_by('date_created')
    if form.validate_on_submit():
        todo = Todo(form.title.data, form.description.data)
        db.session.add(todo)
        db.session.commit()
        flash('Задача добавлена')
        return redirect(url_for('todo'))
    return render_template('todo.html', todos=todos, form=form)


@app.route("/delete/<string:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo'))
