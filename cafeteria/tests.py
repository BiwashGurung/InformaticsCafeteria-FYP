from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class SignupPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_page_renders_correct_template(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeteria/registration.html')

    def test_signup_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())

    def test_signup_passwords_do_not_match(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password456'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_username_already_exists(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class SignupPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_page_renders_correct_template(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeteria/registration.html')

    def test_signup_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())

    def test_signup_passwords_do_not_match(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password456'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_username_already_exists(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class SignupPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_page_renders_correct_template(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeteria/registration.html')

    def test_signup_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())

    def test_signup_passwords_do_not_match(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password456'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_username_already_exists(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)