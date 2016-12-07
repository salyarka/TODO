from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField

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