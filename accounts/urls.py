from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('account_settings', views.account_settings, name='account_settings'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('connections', views.connections, name='connections'),
    path('change_password', views.change_password, name='change_password'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('email_sent', views.email_sent, name='email_sent'),
    path('verify_account', views.verify_account, name='verify_account'),

    # reset password views lists
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
