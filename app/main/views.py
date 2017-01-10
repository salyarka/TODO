from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import datetime
from . import main
from .forms import TodoForm, ListForm
from ..models import Todo, TodoList
from .. import db, login_manager


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))


@main.route("/")
def home():
    return render_template('index.html')


@main.route("/list", methods=['GET', 'POST'])
@login_required
def list():
    form = ListForm()
    if form.validate_on_submit():
        user_id = current_user.id
        todo_list = TodoList(form.title.data, user_id)
        db.session.add(todo_list)
        db.session.commit()
        flash('Список добавлен', 'alert alert-success')
        return redirect(url_for('main.list'))
    return render_template('todolist.html', form=form)


@main.route("/list/<int:list_id>", methods=['DELETE'])
@login_required
def list_del(list_id):
    user_id = current_user.id
    todo_list = TodoList.query.filter_by(
        id=list_id, user_id=user_id).first_or_404()
    db.session.delete(todo_list)
    db.session.commit()
    return redirect(url_for('main.list'))


@main.route("/list/<int:list_id>", methods=['PUT'])
@login_required
def list_edit(list_id):
    user_id = current_user.id
    todo_list = TodoList.query.filter_by(
        id=list_id, user_id=user_id).first_or_404()
    todo_list.title = request.args.get('new_title')
    db.session.commit()
    return redirect(url_for('main.list'))


@main.route("/list/<int:list_id>", methods=['GET', 'POST'])
@login_required
def todo(list_id):
    form = TodoForm()
    user_id = current_user.id
    todo_list = TodoList.query.filter_by(
        id=list_id, user_id=user_id).first_or_404()
    during = todo_list.todos.order_by(
        (Todo.deadline.desc())).filter(Todo.status == 0).all()
    finished = todo_list.todos.filter(Todo.status == 1).all()
    now = datetime.date.today()
    if form.validate_on_submit():
        todo = Todo(form.title.data, todo_list.id, user_id, form.deadline.data)
        db.session.add(todo)
        db.session.commit()
        flash('Задача добавлена', 'alert alert-success')
        return redirect(url_for('main.todo', list_id=list_id))
    return render_template(
        'todo.html', form=form, todo_list=todo_list,
        finished=finished, during=during, now=now)


@main.route("/list/<int:list_id>/<int:todo_id>", methods=['DELETE'])
@login_required
def todo_del(list_id, todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(
        id=todo_id, list_id=list_id, user_id=user_id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.todo', list_id=list_id))


@main.route("/list/<int:list_id>/<int:todo_id>", methods=['PUT'])
@login_required
def todo_edit(list_id, todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(
        id=todo_id, list_id=list_id, user_id=user_id).first_or_404()
    todo.title = request.args.get('new_title')
    todo.description = request.args.get('description')
    db.session.commit()
    return redirect(url_for('main.todo', list_id=list_id))


@main.route("/list/<int:list_id>/<int:todo_id>", methods=['PATCH'])
@login_required
def mark_done(list_id, todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(
        id=todo_id, list_id=list_id, user_id=user_id).first_or_404()
    if todo.status is False:
        todo.status = True
    else:
        todo.status = False
    db.session.commit()
    return redirect(url_for('main.todo', list_id=list_id))
