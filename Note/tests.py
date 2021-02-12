from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User


from Note.models import Note


def create_user(username, password):
    return User.objects.create_user(username=username, password=password)


def create_note(user, title):
    return Note.objects.create(
        user=user, title=title, category='django', text='example', modification_date=timezone.now()
    )


class IndexTests(TestCase):
    def test_index_authenticated(self):
        user = create_user('jan', 'pass')
        note = create_note(user, 'test')

        self.client.login(username='jan', password='pass')
        response = self.client.get('/note/')

        self.assertEqual(user, User.objects.get(username='jan'))
        self.assertIsNotNone(note)
        self.assertContains(response, 'test')

    def test_index_not_authenticated(self):
        user = create_user('jan', 'pass')
        note = create_note(user, 'test')

        response = self.client.get('/note/')

        self.assertEqual(user, User.objects.get(username='jan'))
        self.assertIsNotNone(note)
        self.assertEqual(response.status_code, 302)


class DetailsTest(TestCase):
    def test_details_user_authenticated(self):
        user = create_user('jan', 'pass')
        Note.objects.create(user=user, title='d1', text='', category='django', modification_date=timezone.now())
        Note.objects.create(user=user, title='d2', text='', category='django', modification_date=timezone.now())
        Note.objects.create(user=user, title='nd2', text='', category='django2', modification_date=timezone.now())

        self.client.login(username='jan', password='pass')
        response = self.client.get('/note/details/1')

        self.assertContains(response, 'd1')
        self.assertNotContains(response, 'd2')
        self.assertNotContains(response, 'nd2')

    def test_details_user_not_authenticated(self):
        user = create_user('jan', 'pass')
        Note.objects.create(user=user, title='d1', text='', category='django', modification_date=timezone.now())
        Note.objects.create(user=user, title='d2', text='', category='django', modification_date=timezone.now())
        Note.objects.create(user=user, title='nd2', text='', category='django2', modification_date=timezone.now())

        response = self.client.get('/note/details/)')

        self.assertEqual(response.status_code, 302)

    def test_details_invalid_note(self):
        create_user('jan', 'pass')
        self.client.login(username='jan', password='pass')
        response = self.client.get('/note/details/1')

        self.assertEqual(response.status_code, 404)


class CategoriesTest(TestCase):
    def test_category_not_authenticated(self):
        user = create_user('jan', 'pass')
        Note.objects.create(user=user, title='d1', text='', category='django', modification_date=timezone.now())

        response = self.client.get('/note/category/django')

        self.assertEqual(response.status_code, 302)

    def test_category_authenticated(self):
        user = create_user('jan', 'pass')
        Note.objects.create(user=user, title='d1', text='', category='django', modification_date=timezone.now())
        Note.objects.create(user=user, title='d2', text='', category='django', modification_date=timezone.now())

        self.client.login(username='jan', password='pass')
        response = self.client.get('/note/category/django')

        self.assertContains(response, 'd1')
        self.assertContains(response, 'd2')

    def test_category_not_exist(self):
        user = create_user('jan', 'pass')
        create_note(user, 'test')

        self.client.login(username='jan', password='pass')
        response = self.client.get('/note/category/not_django')

        self.assertEqual(response.status_code, 404)


class LogoutViewTest(TestCase):
    def test_logout_view_logged(self):
        create_user('jan', 'pass')

        self.client.login(username='jan', password='pass')
        response = self.client.get('/note/logout')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You've been logged out")

    def test_logout_view_not_logged(self):
        response = self.client.get('/note/logout')

        self.assertEqual(response.status_code, 404)


class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get('/note/login')
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")
        self.assertContains(response, "Register account")


class RegisterViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get('/note/register')
        self.assertContains(response, 'Frist name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Username:')
        self.assertContains(response, 'E-mail:')
        self.assertContains(response, 'Password:')
