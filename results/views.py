from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
# Create your views here.
from .models import Result
from weeks.models import Week
from games.models import Game


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
            if not results_list:
                games = Game.objects.filter(week=week.id)
                games_list = [game.to_dict() for game in games]
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


def get_results_from_table(week_id, user_id):
    results = Result.objects.filter(week=week_id, user=user_id)
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
