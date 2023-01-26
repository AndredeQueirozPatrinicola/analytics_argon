from django.urls import path, include
from apps.home import views

from rest_framework import routers

from .views import GraduacaoAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('graduacao', GraduacaoAPIView.as_view(), name='graduacao')
]