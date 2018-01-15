# acounts/urls.py
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
]