from tests import Test


class TestGet(Test):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertIn(b'Welcome to Mess Management System', response.data)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertMessageFlashed(
            "No dishes are available in Mess!", category='warning')

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertIn(b'Login', response.data)
        self.assert200(response)
        self.assertTemplateUsed('login.html')

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertIn(b'Register', response.data)
        self.assert200(response)
        self.assertTemplateUsed('register.html')

    def test_balance_page(self):
        response = self.client.get('/balance')
        self.assertRedirects(response, '/')
        self.assertMessageFlashed("You are unauthorized to access the page!",
                                  category='warning')

    def test_order_page(self):
        response = self.client.get('/order')
        self.assertRedirects(response, '/')
        self.assertMessageFlashed("You are unauthorized to access the page!",
                                  category='warning')

    def test_forgot_page(self):
        response = self.client.get('/forgot')
        self.assertIn(b'Reset Password', response.data)
        self.assert200(response)
        self.assertTemplateUsed('reset.html')

    def test_password_reset_page(self):
        response = self.client.get('/forgot/token', follow_redirects=False)
        self.assertIn(b'Reset Password', response.data)
        self.assert200(response)
        self.assertTemplateUsed('reset_password.html')

    def test_logout_page(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')
        self.assertMessageFlashed("You are unauthorized to access the page!",
                                  category='warning')


class TestPost(Test):

    def test_register(self):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')

    def test_dashboard(self):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')

    def test_login(self):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')
        response = self.client.post(
            '/login',
            data=dict(
                email="test@test.com",
                password="testingpassword"
            ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')

    def test_balance(self):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')
        response = self.client.post(
            '/balance',
            data=dict(
                balance=1000
            ),
            follow_redirects=True
        )
        self.assert200(response)
        self.assertMessageFlashed("₹ 1000 was added successfully to your Mess account!",
                                  category='success')
        self.assertIn(b'Welcome Test', response.data)

    def test_order(self):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')
        response = self.client.get(
            '/order',
            follow_redirects=True
        )
        self.assertIn(b'Order Food', response.data)
        self.assert200(response)
        self.assertTemplateUsed('order.html')

    def test_logout(self, ):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')

        response = self.client.get('/logout',)
        self.assertRedirects(response, '/')

    def test_password_reset_email(self):
        response = self.client.post(
            '/register',
            data=dict(name='Test',
                      email="test@test.com",
                      password="testingpassword"
                      ), follow_redirects=True
        )
        self.assertIn(b'Welcome Test', response.data)
        self.assert200(response)
        self.assertTemplateUsed('dashboard.html')
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')
        response = self.client.post(
            '/forgot',
            data=dict(
                email='test@test.com'
            )
        )
        self.assertRedirects(response, '/')
        self.assertMessageFlashed(
            'Email sent successfully!', category='success')
