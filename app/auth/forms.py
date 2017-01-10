from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User


class RegForm(FlaskForm):
    email = StringField(
        'Эл. почта', validators=[
            Required(),
            Length(1, 64),
            Email('Неверный адресс эл. почты.')]
    )
    username = StringField(
        'Имя',
        validators=[
            Required(),
            Length(1, 64),
            Regexp(
                '^[A-ZА-Яa-zа-я][A-ZА-Яa-zа-я0-9_.]*$', 0,
                'Имя может содержать только буквы,'
                ' цифры, точки и подчеркивания'
            )
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            Required(),
            Length(
                6, 8, message='Пароль должен содержать от 6 до 8 символов'),
            EqualTo(
                'password_conf',
                message='Введенные пароли не совпадают.'
            )])
    password_conf = PasswordField(
        'Подтверждение пароля', validators=[Required()])
    submit = SubmitField('Регистрация')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Такая почта уже зарегистрирована.')


class LogForm(FlaskForm):
    email = StringField('Эл. почта', validators=[Required(), Email()])
    password = PasswordField('Пароль', validators=[Required()])
    submit = SubmitField('Войти')
