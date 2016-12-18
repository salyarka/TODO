from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from flask import redirect, url_for


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


# class Todo(db.model):
#   title = 
#   create_date =
#   deadline = 
#   description =
#   tags =
#   user_id =