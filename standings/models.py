from django.db import models

# Create your models here.

from django.db import models
import json
# Create your models here.


class General(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    winner_hits = models.IntegerField(default=0)
    exact_hits = models.IntegerField(default=0)
    difference_hits = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def get_total_points(self):
        points_for_winner_hits = self.winner_hits
        points_for_difference_hits = self.difference_hits * 2
        points_for_exact_hits = self.exact_hits * 3
        return points_for_winner_hits + points_for_difference_hits + points_for_exact_hits

    def to_dict(self):
        return {
            'username': self.user.username,
            'winner_hits': self.winner_hits,
            'difference_hits': self.difference_hits,
            'exact_hits': self.exact_hits,
            'total_points': self.points
        }


class Weekly(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    week = models.ForeignKey('weeks.Week', on_delete=models.CASCADE)
    winner_hits = models.IntegerField(default=0)
    exact_hits = models.IntegerField(default=0)
    difference_hits = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    processed = models.BooleanField(default=False)

    def get_total_points(self):
        points_for_winner_hits = self.winner_hits
        points_for_difference_hits = self.difference_hits * 2
        points_for_exact_hits = self.exact_hits * 3
        return points_for_winner_hits + points_for_difference_hits + points_for_exact_hits

    def to_dict(self):
        return {
            'username': self.user.username,
            'winner_hits': self.winner_hits,
            'difference_hits': self.difference_hits,
            'exact_hits': self.exact_hits,
            'total_points': self.points
        }
