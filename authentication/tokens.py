"""
Extended the PasswordResetTokenGenerator.

Create a unique token generator to confirm email addresses.
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Set token for new accounts."""

    def _make_hash_value(self, user, timestamp):
        """Make use of your project's SECRET_KEY."""
        return (six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.profile.email_confirmed))

account_activation_token = AccountActivationTokenGenerator()
