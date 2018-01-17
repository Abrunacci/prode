"""Unit tests for sign up form."""
from django.test import TestCase

from authentication.forms import SignUpForm


class SignUpFormTest(TestCase):
    """Unit tests the signing up form."""

    def test_form_has_fields(self):
        """Check form has fields: username, email, password1, password2."""
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
