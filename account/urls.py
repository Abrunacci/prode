"""URLs for account app."""
from django.conf.urls import url

from account import views

urlpatterns = [
    url('', views.profile, name='profile'),
    url(r'^save_uploaded_picture/$', views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^picture/$', views.picture, name='picture'),
    url(r'^password/$', views.password, name='password'),
    url(r'^upload_picture/$', views.upload_picture,
        name='upload_picture'),
    ]
