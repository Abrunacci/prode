"""
Extend admin panel with account info.

More info at
https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-the-existing-user-model
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from account.models import Profile


class ProfileInline(admin.StackedInline):
    """Define an inline admin descriptor for Profile mode which acts a bit like a singleton."""

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    """Define a new User admin."""

    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    list_select_related = ('profile', )

    def get_location(self, instance):
        """Return `location` from Profile."""
        return instance.profile.location

    get_location.short_description = 'Location'


# re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
