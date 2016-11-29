class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587 
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	DB_USERNAME = os.environ.get('DB_USERNAME')
	DB_PASSWORD = os.environ.get('DB_PASSWORD')
	SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@localhost/TODO'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True


config = {'default': Config}	

