"""Unit tests for sign up view."""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve

from authentication.forms import SignUpForm
from authentication.views import signup


class SignUpTests(TestCase):
    """Unit tests for signing up process."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        """Resolve sign up URL to sign up view."""
        view = resolve('/auth/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        """Check for Cross-Site Request Forgery prevention."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Present a form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """Check the view contains five inputs.

        csrf, username, email, password1, password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    """Unit tests for successul signing up process."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('signup')
        data = {'username': 'john',
                'email': 'john@doe.com',
                'password1': 'abcdef123456',
                'password2': 'abcdef123456'}
        self.response = self.client.post(url, data)
        self.url_account_activation_sent = reverse('account_activation_sent')
        self.url_home = reverse('home')

    def test_redirection(self):
        """Redirect user to account activation notice."""
        self.assertRedirects(self.response, self.url_account_activation_sent)

    def test_user_creation(self):
        """Crate user."""
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """Check user in new context.

        Create a new request to an arbitrary page,
        and check there is an `user` in its context, after successful sign up.
        It shouldn't be, as the user needs to validate e-mail address.
        """
        response = self.client.get(self.url_home)
        user = response.context.get('user')
        self.assertFalse(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    """Unit tests for unsuccessul signing up process."""

    def setUp(self):
        """Set variables for all tests in class."""
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        """Check page is up."""
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        """Display errors."""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        """Check user still doesn't exist."""
        self.assertFalse(User.objects.exists())
