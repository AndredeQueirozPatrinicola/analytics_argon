from django.urls import path, re_path, include
from django.conf.urls import url 
from django.conf import settings
from apps.home import views

from rest_framework import routers

from .views import DocenteViewSet

router = routers.DefaultRouter()
router.register('api/teste', DocenteViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]