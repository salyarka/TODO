from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import RegForm, TodoForm, LogForm, ListForm, DelForm, EditForm
from app.models import User, Todo, TodoList
from flask_login import login_user, login_required, logout_user, current_user


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def reg():
    form = RegForm()

    # if form.validate... переделать

    if form.validate_username(form.username.data):
        flash('Пользователь с таким именем уже существует.',
              'alert alert-warning')
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
    del_form = DelForm()
    edit_form = EditForm()
    if form.validate_on_submit():
        user_id = current_user.id
        todo_list = TodoList(form.title.data, user_id)
        db.session.add(todo_list)
        db.session.commit()
        flash('Список добавлен', 'alert alert-success')
        return redirect(url_for('list'))
    return render_template('todolist.html',
                           form=form,
                           del_form=del_form,
                           edit_form=edit_form)


@app.route("/list/<int:list_id>", methods=['DELETE'])
@login_required
def list_del(list_id):
    user_id = current_user.id
    todo_list = TodoList.query.filter_by(
        id=list_id, user_id=user_id).first_or_404()
    db.session.delete(todo_list)
    db.session.commit()
    return redirect(url_for('list'))


@app.route("/list/<int:list_id>", methods=['PUT'])
@login_required
def list_edit(list_id):
    user_id = current_user.id
    todo_list = TodoList.query.filter_by(
        id=list_id, user_id=user_id).first_or_404()
    todo_list.title = request.args.get('new_title')
    db.session.commit()
    return redirect(url_for('list'))


@app.route("/list/<int:list_id>", methods=['GET', 'POST'])
@login_required
def todo(list_id):
    form = TodoForm()
    user_id = current_user.id
    todo_list = TodoList.query.filter_by(
        id=list_id, user_id=user_id).first_or_404()
    if form.validate_on_submit():
        todo = Todo(form.title.data, form.description.data,
                    todo_list.id, user_id)
        db.session.add(todo)
        db.session.commit()
        flash('Задача добавлена', 'alert alert-success')
        return redirect(url_for('todo', list_id=list_id))
    return render_template('todo.html', form=form, todo_list=todo_list)


@app.route("/list/<int:list_id>/<int:todo_id>", methods=['DELETE'])
@login_required
def todo_del(list_id, todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(
        id=todo_id, list_id=list_id, user_id=user_id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo', list_id=list_id))


@app.route("/list/<int:list_id>/<int:todo_id>", methods=['PUT'])
@login_required
def todo_edit(list_id, todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(
        id=todo_id, list_id=list_id, user_id=user_id).first_or_404()
    todo.title = request.args.get('new_title')
    db.session.commit()
    return redirect(url_for('todo', list_id=list_id))
