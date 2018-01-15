from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

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
            week_description = json_data.get('week')
            week = Week.objects.get(description=week_description)
            games = Game.objects.filter(week=week.id)
            games_list = [game.to_dict() for game in games]
            from django.http import JsonResponse
            return JsonResponse({"games": games_list})
    weeks = Week.objects.all()
    return render(request,
                  'my_results.html',
                  {
                      'weeks': weeks
                  })
