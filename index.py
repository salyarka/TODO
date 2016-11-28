from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
app.secret_key = '123'
db = SQLAlchemy(app)

class RegForm(FlaskForm ):
	SECRET_KEY = '123'
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

# @app.route ("/todo"):
# def todo():	

if __name__ == "__main__":
    app.run()
    manager.run()

