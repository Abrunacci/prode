"""URLs for authentication app."""
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from authentication import views as authentication_views

urlpatterns = [
    # signup, login, logout
    url(r'^signup/$', authentication_views.signup, name='signup'),
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='authentication/login.html'),
        name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # account activation
    url(r'^account_activation_sent/$',
        authentication_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        authentication_views.activate, name='activate'),

    # password reset
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='authentication/password_reset.html',
            email_template_name='authentication/password_reset_email.html',
            subject_template_name='authentication/password_reset_subject.txt'),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='authentication/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='authentication/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='authentication/password_reset_complete.html'),
        name='password_reset_complete'),

    # authentication pasword change (replaced by account app)
    # url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(
    #     template_name='authentication/password_change.html'),
    #     name='password_change'),
    # url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='authentication/password_change_done.html'),
    #     name='password_change_done'),
    ]
