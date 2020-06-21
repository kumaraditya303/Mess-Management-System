from tests import Test


class TestGet(Test):

    def test_admin_page(self):
        response = self.client.get('/admin/')
        self.assertIn(b'Admin Login', response.data)
        self.assert200(response)
        self.assertTemplateUsed('admin.html')

    def test_dashboard_page(self):
        response = self.client.get('/admin/dashboard')
        self.assertRedirects(response, '/')
        self.assertMessageFlashed("You are unauthorized to access the page!",
                                  category='warning')

    def test_logout_page(self):
        response = self.client.get('/admin/logout')
        self.assertRedirects(response, '/')
        self.assertMessageFlashed("You are unauthorized to access the page!",
                                  category='warning')

    def test_add_dish_page(self):
        response = self.client.get('/admin/add/dishes')
        self.assertRedirects(response, '/')
        self.assertMessageFlashed("You are unauthorized to access the page!",
                                  category='warning')
