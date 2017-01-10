import os


class DefaultConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USERNAME + \
        ':' + DB_PASSWORD + '@localhost/TODO'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DefaultConfig.DB_USERNAME + \
        ':' + DefaultConfig.DB_PASSWORD + '@localhost/TODO-TEST'
