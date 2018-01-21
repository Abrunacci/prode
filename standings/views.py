from django.shortcuts import render
import json
from django.contrib.auth.models import User
# Create your views here.
from .models import General, Weekly
from django.views.decorators.csrf import csrf_exempt
from home.models import Settings
from games.models import Game
from results.models import Result
from django.http import JsonResponse


def get_general_standings():
    general_standing = General.objects.filter().order_by('-points',
                                                         '-exact_hits',
                                                         '-difference_hits',
                                                         '-winner_hits',
                                                         'user__username')
    general_standing = [standing.to_dict() for standing in general_standing]
    return general_standing


def get_weekly_standings():
    settings = Settings.objects.get(id=1)
    weekly_standing = Weekly.objects.filter(week_id=settings.current_week_id).order_by('-points',
                                                                                       '-exact_hits',
                                                                                       '-difference_hits',
                                                                                       '-winner_hits',
                                                                                       'user__username')
    weekly_standing = [standing.to_dict() for standing in weekly_standing]
    return weekly_standing


def get_user_points(request, user_id):
    settings = Settings.objects.get(id=1)
    user_points = dict()
    weekly_points = Weekly.objects.filter(user_id=user_id, week_id=settings.current_week_id).first()
    general_points = General.objects.filter(user_id=user_id).first()
    if request.is_ajax():
        user_points = {
            'weekly': weekly_points.get_total_points() if weekly_points else 0,
            'general': general_points.get_total_points() if general_points else 0
        }
    return user_points


def generate_weekly_standings():
    settings = Settings.objects.get(id=1)
    games = Game.objects.filter(week_id=settings.current_week_id, finished=True)
    for user in User.objects.filter(is_superuser=False).all():
        current_stand = Weekly.objects.filter(user=user.id, week_id=settings.current_week_id).first()
        if not current_stand:
            current_stand = Weekly()
        for game in games:
            user_results = Result.objects.filter(user=user, week_id=settings.current_week_id, game_id=game.id, processed=False).first()
            if not user_results:
                continue
            if game.get_winner() == user_results.get_winner():
                current_stand.winner_hits += 1
                if game.get_difference() == user_results.get_difference():
                    current_stand.difference_hits += 1
                if game.home_team_score == user_results.home_score and game.away_team_score == user_results.away_score:
                    current_stand.exact_hits += 1
            user_results.processed = True
            user_results.save()
        current_stand.week = settings.current_week
        current_stand.user = user
        current_stand.points = current_stand.get_total_points()
        current_stand.save()


def generate_general_standings():
    settings = Settings.objects.get(id=1)
    for user in User.objects.filter(is_superuser=False).all():
        current_stand = General.objects.filter(user=user.id).first()
        weekly_standings = Weekly.objects.filter(user_id=user.id, processed=False)
        if not current_stand:
            current_stand = General()
        for week_stand in weekly_standings:
            current_stand.winner_hits += week_stand.winner_hits
            current_stand.difference_hits += week_stand.difference_hits
            current_stand.exact_hits += week_stand.exact_hits
            week_stand.processed = True
            week_stand.save()
        current_stand.user = user
        current_stand.points = current_stand.get_total_points()
        current_stand.save()


@csrf_exempt
def generate_tables(request):
    if request.is_ajax():
        if request.method == 'POST':
            user_id = json.loads(request.body).get('user_id')
            data = {
                'weekly': get_weekly_standings(),
                'general': get_general_standings(),
                'user_points': get_user_points(request, user_id),
            }
            return JsonResponse(data)