import unittest
from app import app, db
from app.models import User


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.config.from_object('app.config.TestingConfig')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_authenticate_user(self):
        user = User('lala@mail.ru', 'John', '123456')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.authenticate('123456'))
