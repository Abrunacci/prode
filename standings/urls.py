from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('general/', views.get_general_standings, name='general_standings'),
    path('weekly/', views.get_weekly_standings, name='weekly_standing'),
    path('get_tables/', views.generate_tables, name='get_tables'),
    path('generate/', views.generate_general_standings, name='generate')
]