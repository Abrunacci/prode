from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
# Create your views here.
from .models import Result
from weeks.models import Week
from games.models import Game
from home.models import Settings


def all_results(request):
    results = Result.objects.all().order_by('user')
    return render(request, 'all_results.html', {'results': results})


@csrf_exempt
def my_results(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            week_id = json_data.get('week')
            week = Week.objects.get(id=week_id)
            results_list = get_results_from_table(week.id, json_data.get('user_id'))
            current_week = Settings.objects.get(id=1)
            if current_week.current_week_id > week.id:
                return JsonResponse({'error': 'No se pueden cargar predicciones de fechas anteriores a la actual.'})
            from django.utils import timezone
            time = timezone.now()
            if not results_list:
                games = Game.objects.filter(week=week.id, finished=False)
                games_list = list()
                for game in games:
                    if game.game_day > time:
                        games_list.append(game.to_dict())
                if not games_list:
                    return JsonResponse({})
                return JsonResponse({"games": games_list})
            return JsonResponse({'results': results_list})
    weeks = Week.objects.all()
    return render(request,
                  'my_results.html',
                  {
                      'weeks': weeks
                  })


@csrf_exempt
def other_user_results(request):
    if request.is_ajax():
        if request.method == 'POST':
            current_week = Settings.objects.get(id=1)
            json_data = json.loads(request.body)
            current_user_results = get_results_from_table(week_id=json_data.get('week'),
                                                          user_id=json_data.get('current_user'))
            if not current_user_results:
                if current_week.current_week_id <= int(json_data.get('week')):
                    return JsonResponse({'error': 'Debe cargar los resultados de la semana deseada para poder ver los de los rivales.'})
            other_user_results = get_results_from_table(week_id=json_data.get('week'),
                                                        user_id=json_data.get('user_id'),
                                                        processed=True)
            if not other_user_results:
                return JsonResponse({'error': 'El usuario no ha cargado los resultados de la semana seleccionada o los partidos no han finalizado.'})
            return JsonResponse({'results': other_user_results})
    weeks = Week.objects.all()
    users = User.objects.all()
    return render(request,
                  'all_results.html',
                  {
                      'weeks': weeks,
                      'users': users
                  })


def get_results_from_table(week_id, user_id, processed=False):
    results = Result.objects.filter(week=week_id, user=user_id, processed=processed)
    results_list = [result.to_dict() for result in results]
    return results_list


@csrf_exempt
def save_user_results(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            for result in json_data.get('results'):
                user_result = Result()
                user_result.week_id = result.get('week_id')
                user_result.away_score = result.get('away_team_score') if result.get('away_team_score') else 0
                user_result.home_score = result.get('home_team_score') if result.get('home_team_score') else 0
                user_result.game_id = result.get('game_id')
                user_result.user_id = result.get('user_id')
                user_result.save()
        return JsonResponse({'saved': 'success'})
    return JsonResponse({'saved': 'error'})
