import unittest
from flask import url_for
from app import app, db
from app.models import User, TodoList


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.config.from_object('app.config.TestingConfig')
        self.test_client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def make_user(self):
        user = User('lala@mail.ru', 'John', '123456')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username='John').first()
        return user

    def make_client(self, user_obj):
        with self.test_client as client:
            with client.session_transaction() as session:
                session['user_id'] = user_obj.id
                session['_fresh'] = True
        return client

    def make_list(self, user_obj):
        todo_list = TodoList('title', user_obj.id)
        db.session.add(todo_list)
        db.session.commit()
        todo_list = TodoList.query.filter_by(user_id=user_obj.id).first()
        return todo_list

    def test_list_get(self):
        user = self.make_user()
        client = self.make_client(user)
        resp = client.get('list')
        self.assertEqual(resp.status_code, 200)

    def test_list_del(self):
        user = self.make_user()
        todo_list = TodoList('title', user.id)
        db.session.add(todo_list)
        db.session.commit()
        client = self.make_client(user)
        resp = client.delete('/list/' + str(todo_list.id))
        self.assertEqual(resp.status_code, 302)

    def test_list_edit(self):
        user = self.make_user()
        todo_list = TodoList('title', user.id)
        db.session.add(todo_list)
        db.session.commit()
        client = self.make_client(user)
        resp = client.put('/list/' + str(todo_list.id),
                          data={'new_title': 'title'})
        self.assertEqual(resp.location, url_for('main.list', _external=True))

    def test_todo_get(self):
        user = self.make_user()
        todo_list = TodoList('title', user.id)
        db.session.add(todo_list)
        db.session.commit()
        client = self.make_client(user)
        resp = client.get('/list/' + str(todo_list.id))
        self.assertEqual(resp.status_code, 200)

    def test_todo_post(self):
        user = self.make_user()
        todo_list = TodoList('title', user.id)
        db.session.add(todo_list)
        db.session.commit()
        client = self.make_client(user)
        resp = client.post('/list/' + str(todo_list.id),
                           data={'title': 'title'})
        self.assertEqual(resp.location, url_for(
            'main.todo', list_id=todo_list.id, _external=True))
