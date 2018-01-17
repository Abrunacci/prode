"""Tests for account app."""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase


class TestViews(TestCase):
    """Includes tests for all the functionality associated with Views."""

    def setUp(self):
        """."""
        self.client = Client()
        self.other_client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
            )
        self.other_user = get_user_model().objects.create_user(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
            )
        self.client.login(username='test_user', password='top_secret')

    def test_get_profile_response(self):
        """."""
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)

    def test_post_profile_response(self):
        """."""
        response = self.client.post(reverse('account:profile'),
                                    {'first_name': 'first_name',
                                     'last_name': 'last_name'})
        self.assertEqual(response.status_code, 200)

    def test_get_picture_response(self):
        """."""
        response = self.client.get(reverse('account:picture'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('uploaded_picture' in response.context)
        self.assertEqual(response.context['uploaded_picture'], False)

    def test_post_picture_response(self):
        """."""
        response = self.client.get(
            reverse('account:picture'), {'account:linked_accounts': 'uploaded'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('uploaded_picture' in response.context)
        self.assertEqual(response.context['uploaded_picture'], True)
