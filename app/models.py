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
  username = db.Column(db.String(64), unique=True)
  password_hash = db.Column(db.String(128))


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

  def __init__(self, title, description):
    self.title = title
    self.description = description


# Тралала здесь все потерял, были контролеры типа delete/<string:todo_id> 
# и delete/<string:todo_id>