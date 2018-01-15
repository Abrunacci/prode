# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from registration.views import RegistrationForm, RegistrationView
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(RegistrationView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = '../templates/registration_form.html'