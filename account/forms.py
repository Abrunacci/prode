"""Forms for account app."""
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from account.models import Profile


class ChangePasswordForm(forms.ModelForm):
    """Make form to change password."""

    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        label="Old password",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )
    new_password = forms.CharField(
        label="New password",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )
    confirm_password = forms.CharField(
        label="Confirm new password",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )

    class Meta(object):
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        """Cleanup variables."""
        super(ChangePasswordForm, self).clean()

        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)

        if not user.check_password(old_password) and user.has_usable_password():
            self._errors['old_password'] = self.error_class(['Old password don\'t match'])

        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class(['Passwords don\'t match'])

        return self.cleaned_data