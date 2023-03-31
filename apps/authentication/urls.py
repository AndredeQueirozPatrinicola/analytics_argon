from django.urls import path 
from django.contrib.auth.views import LogoutView
from django_oauth_usp.accounts.views import accounts_authorize, accounts_login


urlpatterns = [
    path('login', accounts_login, name='login'),
    path('authorize', accounts_authorize, name='authorize'),
    path('logout', LogoutView.as_view(), name='logout')
]
