from Mess_Management_System import app, db, mail
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
        pass


class TestGet(Test):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertIn(b'Welcome to Mess Management System', response.data)

    # def test_login_page(self):
    #     response = self.client.get('/login')
    #     self.assertIn(b'Login', response.data)

    # def test_register_page(self):
    #     response = self.client.get('/register')
    #     self.assertIn(b'Register', response.data)

    def test_admin_page(self):
        response = self.client.get('/admin')
        self.assertIn(b'Admin Login', response.data)
