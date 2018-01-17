"""Unit tests for resetting password (view)."""
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.core import mail
from django.test import TestCase
from django.urls import resolve
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetTests(TestCase):
    """Unit tests for resetting the password (views)."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Check view for resetting password."""
        view = resolve('/auth/reset/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        """Check for Cross-Site Request Forgery prevention."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Check form for resetting password."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """Check for CSRF and email inputs."""
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    """Unit tests after sucessfully resetting the password."""

    def setUp(self):
        """Set variables for all tests in class."""
        email = 'john@doe.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        """Redirect to `password_reset_done` view."""
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        """Check email is on queue."""
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    """Unit tests after unsucessfully resetting the password."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    def test_redirection(self):
        """Redirect to `password_reset_done`."""
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        """Check no email is on queue."""
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    """Unit tests after unsucessfully resetting the password."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Check view for resetting password done."""
        view = resolve('/auth/reset/done/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    """Unit tests for confirming resetting the password."""

    def setUp(self):
        """Set variables for all tests in class.

        Create a valid password reset token.
        Based on how django creates the token internally:
        https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        """
        user = User.objects.create_user(username='john',
                                        email='john@doe.com',
                                        password='123abcdef')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Check view for resetting password confirmation."""
        view = resolve('/auth/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEqual(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        """Check for Cross-Site Request Forgery prevention."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        """Check for two inputs: CSRF and two password fields."""
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    """Unit tests for after confirming resetting the password."""

    def setUp(self):
        """Set variables for all tests in class."""
        user = User.objects.create_user(username='john',
                                        email='john@doe.com',
                                        password='123abcdef')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        # invalidate the token by changing the password
        user.set_password('abcdef123')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_html(self):
        """Check resetting password link in HTML code."""
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):
    """Unit tests for completing resetting the password."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Check view for resetting password complete."""
        view = resolve('/auth/reset/complete/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetCompleteView)
