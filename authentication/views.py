"""Authentication app views."""
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _

from authentication.forms import SignUpForm

from .tokens import account_activation_token


def account_activation_sent(request):
    """Render account activation page."""
    return render(request, 'authentication/account_activation_sent.html', {})


def activate(request, uidb64, token):
    """Process token."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True

        user.save()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, _('Your e-mail has been verified!'))

        return redirect('home')
    else:
        return render(request, 'authentication/account_activation_invalid.html')


def signup(request):
    """Render sign up view."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = _('Activá tu cuenta del Prode Mundialista')
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message)

            return redirect('account_activation_sent')

    else:
        form = SignUpForm()

    return render(request, 'authentication/signup.html', {'form': form, 'view': 'signup'})
