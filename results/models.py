from django.db import models

# Create your models here.


class Result(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    away_score = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.away_score

    def get_away_team(self):
        return self.game.away_team

    def get_home_team(self):
        return self.game.home_team

    def get_away_score(self):
        return self.away_score

    def get_home_score(self):
        return self.home_score