from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('rules/', views.RulesPageView.as_view(), name='rules')
]
