from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import Required, Length, Email, Regexp,\
    EqualTo, Optional
from app.models import User


class TodoForm(FlaskForm):
    title = StringField('Новая задача', validators=[Required()])
    description = StringField('Описание')
    deadline = DateField('Pick a Date', format="%d.%m.%Y",
                         validators=[Optional()])
    create = SubmitField('Создать')


class RegForm(FlaskForm):
    email = StringField(
        'Эл. почта', validators=[Required(),
                                 Length(1, 64),
                                 Email('Неверный адресс эл. почты.')]
    )
    username = StringField('Имя',
                           validators=[
                               Required(),
                               Length(1, 64),
                               Regexp(
                                   '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                   'Имя может содержать только буквы,'
                                   ' цифры, точки и подчеркивания'
                               )
                           ]
                           )
    password = PasswordField('Пароль',
                             validators=[
                                 Required(),
                                 EqualTo(
                                     'password_conf',
                                     message='Введенные пароли не совпадают.'
                                 )])
    password_conf = PasswordField(
        'Подтверждение пароля', validators=[Required()])
    submit = SubmitField('Регистрация')

    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            # raise ValidationError('Такая почта уже зарегистрированна.')
            return True


class LogForm(FlaskForm):
    email = StringField('Эл. почта', validators=[Required(), Email()])
    password = PasswordField('Пароль', validators=[Required()])
    submit = SubmitField('Войти')


class ListForm(FlaskForm):
    title = StringField('Новый список', validators=[Required()])
    create = SubmitField('Создать')


class DelForm(FlaskForm):
    submit = SubmitField('Удалить')


class EditForm(FlaskForm):
    new_title = StringField(validators=[Required()])
    submit = SubmitField('Изменить')
