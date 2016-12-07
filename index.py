from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@localhost/TODO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)
app.secret_key = os.environ.get('SECRET_KEY')

# app = Flask(__name__)
# app.config.from_object(config[config_name])
# config[config_name].init_app(app)
# bootstrap.init_app(app)
# db.init_app(app)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # bootstrap.init_app(app)
    # db.init_app(app)
    return app



class Test(db.Model):
	__tablename__ = 'test'
	id = db.Column('id', db.Integer, primary_key=True)
	data = db.Column('data', db.Unicode)
	# ?end of class?

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.password_hash = password_hash	

# class Todo(db.model):
    # title = 
    # create_date =
    # deadline = 
    # description =
    # tags =
    # user_id = 

class TodoForm(FlaskForm):
    title = StringField()
    deadline = DateField()
    description = StringField()
    tags = StringField()
    create = SubmitField()
    
   

class RegForm(FlaskForm ):
	email = StringField()
	email_conf = StringField('Confirm Email')
	name = StringField()
	password = PasswordField()
	password_conf = PasswordField('Confirm Password')
	submit = SubmitField('Register')


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def reg():
	if request.method == 'GET':
		form = RegForm()
		return render_template('register.html', form=form)
	# else:	

@app.route ("/todo")
def todo():	
    form = TodoForm()
    return render_template('todo.html', form=form)

if __name__ == '__main__':
    manager.run()