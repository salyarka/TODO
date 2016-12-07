from app import app
from flask import render_template, request
from app.forms import RegForm, TodoForm 

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