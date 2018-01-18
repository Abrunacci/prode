from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_results, name='results'),
    path('my_results/', views.my_results, name='my_results'),
    path('save_results/', views.save_user_results, name='save_results')
]
