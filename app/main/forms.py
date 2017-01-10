from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import Required, Optional


class TodoForm(FlaskForm):
    title = StringField('Новая задача', validators=[Required()])
    deadline = DateField('Дата окончания', format="%d.%m.%Y",
                         validators=[Optional()])
    create = SubmitField('Создать')


class ListForm(FlaskForm):
    title = StringField('Новый список', validators=[Required()])
    create = SubmitField('Создать')
