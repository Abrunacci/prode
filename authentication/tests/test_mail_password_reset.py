"""Unit tests for resetting password (email)."""
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class PasswordResetMailTests(TestCase):
    """Unit tests for resetting the password (email)."""

    def setUp(self):
        """Set variables for all tests in class."""
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.response = self.client.post(reverse('password_reset'), {'email': 'john@doe.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        """Check subject integrity."""
        self.assertEqual('[Ojumble] Please reset your password', self.email.subject)

    def test_email_body(self):
        """Check name, emaild and reset token in email body."""
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm',
                                           kwargs={'uidb64': uid, 'token': token})
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn('john@doe.com', self.email.body)

    def test_email_to(self):
        """Check send to address."""
        self.assertEqual(['john@doe.com', ], self.email.to)
