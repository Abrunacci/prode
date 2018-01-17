"""Models for account app."""
import hashlib
import os.path
import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Extend user model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        """String representation."""
        return self.user.username

    def get_picture(self):
        """Search for the user pic, if not try Gravatar, is not set generic."""
        no_picture = 'https://www.ojumble.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):  # pragma: no cover
                return picture_url
            else:  # pragma: no cover
                gravatar_hash = hashlib.md5(self.user.email.lower().encode('utf-8')).hexdigest()
                gravatar_params = urllib.parse.urlencode({'d': no_picture, 's': '256'})
                gravatar_url_base = 'https://www.gravatar.com/avatar/{0}?{1}'
                gravatar_url = gravatar_url_base.format(gravatar_hash, gravatar_params)

                return gravatar_url

        except Exception:
            return no_picture

    def get_screen_name(self):
        """Return full name, if availalbe, or else username."""
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except Exception:
            return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """Hook the `update_user_profile` methods to the User model.

    Whenever a save event occurs.
    """
    if created:
        Profile.objects.create(user=instance)

    instance.profile.save()
