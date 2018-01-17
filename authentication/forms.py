"""Online forms for authentication app."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django import forms


class SignUpForm(UserCreationForm):
    """Specs for sign up form."""

    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta(object):
        """Nada."""

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        except MultipleObjectsReturned:

            # A user was found with this as a username, raise an error.
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
