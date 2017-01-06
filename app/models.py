from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from flask import redirect, url_for
from datetime import datetime


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    todo_lists = db.relationship(
        'TodoList', cascade="all, delete-orphan", backref='users')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self.password_hash, password)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    date_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=0)
    deadline = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, list_id, user_id, deadline=None):
        self.title = title
        self.description = description
        self.list_id = list_id
        self.user_id = user_id
        self.deadline = deadline


class TodoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    todos = db.relationship(
        'Todo', cascade="all, delete-orphan", backref='todo_list')

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
