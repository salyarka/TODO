from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import RegForm, TodoForm, LogForm, ListForm
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
        flash('Пользователь с таким именем уже существует.', 'alert alert-warning')
        return render_template('register.html', form=form)

    if form.validate_email(form.email.data):
        flash('Такой email уже зарегистрирован.', 'alert alert-warning')
        return render_template('register.html', form=form)

    if form.validate_on_submit():
        user = User(form.email.data, form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно', 'alert alert-success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LogForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.authenticate(form.password.data):
            login_user(user)
            flash('Вход произошел успешно', 'alert alert-success')
            return redirect(url_for('list'))
        flash('Неверная эл. почта или пароль', 'alert alert-warning')
    return render_template('login.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'alert alert-warning')
    return redirect(url_for('home'))


@app.route("/list", methods=['GET', 'POST'])
@login_required
def list():
    form = ListForm()
    if form.validate_on_submit():
        todo_list = TodoList(form.title.data, form.user_id.data)
        db.session.add(todo_list)
        db.session.commit()
        flash('Список добавлен', 'alert alert-success')
        return redirect(url_for('list'))
    return render_template('todolist.html', form=form)


@app.route("/list/<int:list_id>", methods=['DELETE'])
@login_required
def list_del(list_id):
  list_id = request.args.get('list_id')
  todo_list = TodoList.query.filter_by(id=list_id).first()
  db.session.delete(todo_list)
  db.session.commit()
  return redirect(url_for('list'))




@app.route("/list/<int:list_id>", methods=['GET', 'POST'])
@login_required
def todo():
    form = TodoForm()
    todos = Todo.query.order_by('date_created')
    if form.validate_on_submit():
        todo = Todo(form.title.data, form.description.data)
        db.session.add(todo)
        db.session.commit()
        flash('Задача добавлена', 'alert alert-success')
        return redirect(url_for('todo'))
    return render_template('todo.html', todos=todos, form=form)


# @app.route("/delete/<string:todo_id>")
# def delete(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     db.session.delete(todo)
#     db.session.commit()
#     return redirect(url_for('todo'))


# @app.route("/list/<id>", methods=['GET', 'POST'])  
# def todo():
# список задач в заданном листе
# 
# @app.route("/list/<id>/delete/<todo_id>") / @app.route("/list/<id>/edit/<todo_id>", methods=['POST', 'DELETE'])
# def delete():                               def edit();
# удаление задачи                             POST - изменяем задачу DELETE - удаляем
# 
# @app.route("/list/<id>/edit/<todo_id>")
# def edit():
# изменение задачи
# 
# @app.route("/list/delete/<id>")
# def deleteList():
# удаление листа
# 
# @app.route("/list/edit/<id>")
# def editList():
# изменение листа