from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_modus import Modus


app = Flask(__name__)
modus = Modus(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.config.from_object('app.config')

import app.views