import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587 
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@hostname/database'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True