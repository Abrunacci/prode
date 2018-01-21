from django.views.generic import TemplateView
from django.shortcuts import render
# Create your views here.


def HomePageView(request):
    return render(request, 'home.html', {'range': range(1,100)})


class AboutPageView(TemplateView):
    template_name = 'about.html'


class RulesPageView(TemplateView):
    template_name = 'rules.html'
