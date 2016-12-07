from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import RegForm, TodoForm
from app.models import User


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def reg():
	form = RegForm()
	if form.validate_on_submit():
		user = User(form.email.data, form.name.data, form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Регистрация прошла успешно')
		return redirect(url_for('home'))
	return render_template('register.html', form=form)   	


@app.route ("/todo")
def todo():	
    form = TodoForm()
    return render_template('todo.html', form=form)
