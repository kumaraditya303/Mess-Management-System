from runserver import app, db
from Mess_Management_System import mail
from flask_testing import TestCase
from config import TestConfig


class Test(TestCase):

    def create_app(self):
        app.config.from_object(TestConfig)
        mail.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
