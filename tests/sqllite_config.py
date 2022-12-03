import unittest
from todo_list.app import app, db
from todo_list.configuration.sqlite_database import SQLALCHEMY_DATABASE_URL


class UserTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
        self.app = app.test_client()
        db.create_all()