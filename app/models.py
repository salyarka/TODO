from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))


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
<<<<<<< HEAD
  __tablename__ = 'todo'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128))
  description = db.Column(db.Text)
  date_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)

  def __init__(self, title, description):
    self.title = title
    self.description = description


# Тралала здесь все потерял, были контролеры типа delete/<string:todo_id> 
# и delete/<string:todo_id>
=======
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    date_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=0)
    deadline = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, list_id, user_id, deadline=None):
        self.title = title
        self.list_id = list_id
        self.user_id = user_id
        self.deadline = deadline


class TodoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    todos = db.relationship(
        'Todo', cascade="all, delete-orphan",
        backref='todo_list', lazy='dynamic')

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
>>>>>>> resourcesInUrl
