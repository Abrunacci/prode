"""Views for account app."""
import os

from PIL import Image

from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext as _

from account.forms import ChangePasswordForm


@login_required
@transaction.atomic
def profile(request):
    """Render profile view."""
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
        else:
            messages.error(request, _('No se pudo modificar su contraseña'))
    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'account/profile.html', {
                      'form': form
                   })


@login_required
def picture(request):
    """Render picture view."""
    uploaded_picture = False

    try:
        if request.GET.get('account:upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:  # pragma: no cover
        pass

    return render(request, 'account/picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
def password(request):
    """Render view password view."""
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, _('Su contraseña se guardo correctamente.'))

            return redirect('account:password')
    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'account/password.html', {'form': form})


@login_required
def upload_picture(request):
    """Render uploading picture view."""
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'

        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)

        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'

        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        im = Image.open(filename)
        width, height = im.size

        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/account/picture/?upload_picture=uploaded')

    except Exception:
        return redirect('/account/picture/')


@login_required
def save_uploaded_picture(request):
    """Render saving uploaded picture view."""
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('/account/picture/')
