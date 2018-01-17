"""Unit tests for autentication template tags."""
from django import forms
from django.test import TestCase

from authentication.templatetags.form_tags import field_type
from authentication.templatetags.form_tags import input_class


class ExampleForm(forms.Form):
    """Example form."""

    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(object):
        fields = ('name', 'password')


class FieldTypeTests(TestCase):
    """Field type tests."""

    def test_field_widget_type(self):
        """Field widget type."""
        form = ExampleForm()
        self.assertEqual('TextInput', field_type(form['name']))
        self.assertEqual('PasswordInput', field_type(form['password']))


class InputClassTests(TestCase):
    """Input class tests."""

    def test_unbound_field_initial_state(self):
        """Initial state of unbound field."""
        form = ExampleForm()  # unbound form
        self.assertEqual('form-control ', input_class(form['name']))

    def test_valid_bound_field(self):
        """Valid bound field."""
        form = ExampleForm({'name': 'john', 'password': '123'})  # bound form (field + data)
        self.assertEqual('form-control is-valid', input_class(form['name']))
        self.assertEqual('form-control ', input_class(form['password']))

    def test_invalid_bound_field(self):
        """Invalid bound field."""
        form = ExampleForm({'name': '', 'password': '123'})  # bound form (field + data)
        self.assertEqual('form-control is-invalid', input_class(form['name']))
