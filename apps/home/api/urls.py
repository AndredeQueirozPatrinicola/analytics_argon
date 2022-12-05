from email.mime import base
from django.urls import path, re_path, include
from django.conf.urls import url 
from django.conf import settings
from apps.home import views

from rest_framework import routers

from .views import hello_world

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('teste', hello_world)
]