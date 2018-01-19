from django.db import models
import json
from django.db.models.signals import post_save
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
        return '%s: %s - %s' % (self.week.description, self.away_team.name, self.home_team.name)

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

    def get_winner(self):
        if self.away_team_score > self.home_team_score:
            return self.away_team.name
        if self.home_team_score > self.away_team_score:
            return self.home_team.name

    def get_difference(self):
        if self.away_team_score > self.home_team_score:
            return self.away_team_score - self.home_team_score
        if self.home_team_score > self.away_team_score:
            return self.home_team_score - self.away_team_score


def generate_standings(sender, **kwargs):
    game_instance = kwargs.get('instance')
    if game_instance.finished:
        from standings.views import generate_weekly_standings
        generate_weekly_standings()

post_save.connect(generate_standings, sender=Game)
