from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_script import Manager

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
    manager.run()
    create_app().run(debug=True)