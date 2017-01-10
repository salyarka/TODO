import unittest
from app import app, db


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.config.from_object('app.config.TestingConfig')
        self.test_client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_and_login(self):
        reg_resp = self.test_client.post('/register', data={
            'email': 'lala@mail.ru',
            'username': 'John',
            'password': '123456',
            'password_conf': '123456'})
        self.assertEqual(reg_resp.status_code, 302)
        login = self.test_client.post('/login', data={
            'email': 'lala@mail.ru',
            'password': '123456'
        })
        self.assertEqual(login.status_code, 302)
