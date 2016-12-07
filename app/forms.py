from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

class TodoForm(FlaskForm):
    title = StringField(validators=[Required()])
    deadline = DateField()
    description = StringField()
    tags = StringField()
    create = SubmitField()
    
   

class RegForm(FlaskForm ):
	email = StringField('Эл. почта', validators=[Required(), Length(1, 64),
                                             Email()])
	name = StringField('Имя', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Имя может содержать только буквы, '
                                          'цифры, точки и подчеркивания')])
	password = PasswordField('Пароль', validators=[
        Required(), EqualTo('password_conf', message='Passwords must match.')])
	password_conf = PasswordField('Подтверждение пароля', validators=[Required()])
	submit = SubmitField('Регистрация')