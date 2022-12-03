from flask_testing import TestCase
from todo_list.app import db, app


class SQLiteConfig(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config.from_object("todo_list.configuration.sqlite_database.Config")
        try:
            db.init_app(app)
        except AssertionError: #TODO no idea why it's not working here :D to check why context is not teared down after each request
            pass
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
