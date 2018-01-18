from django.db import models
from django.db.models.signals import post_save
# Create your models here.


class Settings(models.Model):
    current_week = models.ForeignKey('weeks.Week', on_delete=models.CASCADE)


def toppings_changed(sender, **kwargs):
    from standings.views import generate_general_standings, generate_weekly_standings
    generate_weekly_standings()
    generate_general_standings()

post_save.connect(toppings_changed, sender=Settings)
