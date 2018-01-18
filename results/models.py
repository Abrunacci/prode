from django.db import models
import json
# Create your models here.


class Result(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    week = models.ForeignKey('weeks.Week', on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    away_score = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)
    processed = models.BooleanField(default=False)

    def get_winner(self):
        if self.away_score > self.home_score:
            return self.game.away_team.name
        if self.home_score > self.away_score:
            return self.game.home_team.name

    def get_difference(self):
        if self.away_score > self.home_score:
            return self.away_score - self.home_score
        if self.home_score > self.away_score:
            return self.home_score - self.away_score

    def get_away_team(self):
        return self.game.away_team

    def get_home_team(self):
        return self.game.home_team

    def get_away_score(self):
        return self.away_score

    def get_home_score(self):
        return self.home_score

    def __str__(self):
        data = {
            'id': self.id,
            'week': self.week.description,
            'game_id': self.game_id,
            'home_team': {
                'name': self.game.home_team.name,
                'id': self.game.home_team_id,
                'score': self.home_score
            },
            'away_team': {
                'name': self.game.away_team.name,
                'id': self.game.away_team_id,
                'score': self.away_score
            },
        }
        return json.dumps(data)

    def to_dict(self):
        data = {
            'id': self.id,
            'week': self.week.description,
            'game_id': self.game_id,
            'home_team': {
                'name': self.game.home_team.name,
                'id': self.game.home_team_id,
                'score': self.home_score
            },
            'away_team': {
                'name': self.game.away_team.name,
                'id': self.game.away_team_id,
                'score': self.away_score
            },
        }
        return json.dumps(data)