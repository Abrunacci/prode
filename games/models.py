from django.db import models
import json
# Create your models here.


class Game(models.Model):
    week = models.ForeignKey('weeks.Week', on_delete=models.CASCADE)
    home_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='away_team')
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    game_day = models.DateTimeField()
    finished = models.BooleanField(default=False)

    def __str__(self):
        data = {
            'id': self.id,
            'week': self.week.description,
            'home_team': {
                'name': self.home_team.name,
                'id': self.home_team_id,
                'score': self.away_team_score
            },
            'away_team': {
                'name': self.away_team.name,
                'id': self.away_team_id,
                'score': self.away_team_score
            },
        }
        return json.dumps(data)

    def to_dict(self):
        data = {
            'id': self.id,
            'week': self.week.description,
            'home_team': {
                'name': self.home_team.name,
                'id': self.home_team_id,
                'score': self.away_team_score
            },
            'away_team': {
                'name': self.away_team.name,
                'id': self.away_team_id,
                'score': self.away_team_score
            },
        }
        return json.dumps(data)

    def get_home_team(self):
        return self.home_team.name