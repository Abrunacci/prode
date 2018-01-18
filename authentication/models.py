from django.db import models
from django.contrib.auth.models import User
from standings.models import General, Weekly
# Create your models here.
from django.db.models.signals import post_save
from home.models import Settings


def insert_into_standings(sender, **kwargs):
    user_instance = kwargs.get('instance')
    if user_instance.is_active:
        if user_instance.is_superuser:
            return
        week = Settings.objects.get(id=1)
        general_stand = General.objects.filter(user_id=user_instance.id).first()
        if user_instance.is_superuser:
            return
        if not general_stand:
            new_user_stand = General()
            new_user_stand.user = user_instance
            new_user_stand.save()
        weekly_stand = Weekly.objects.filter(user_id=user_instance.id, week_id=week.current_week_id).first()
        if not weekly_stand:
            new_user_weekly_stand = Weekly()
            new_user_weekly_stand.week = week.current_week
            new_user_weekly_stand.user = user_instance
            new_user_weekly_stand.save()


post_save.connect(insert_into_standings, sender=User)
