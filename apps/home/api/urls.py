from django.urls import path, include
from apps.home import views

from rest_framework import routers

from .views import GraduacaoRacaAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('graduacao/raca-por-ano', GraduacaoRacaAPIView.as_view(), name='graduacao'),
    path('graduacao/raca-por-ano/<str:graduacao>', GraduacaoRacaAPIView.as_view(), name='graduacao'),
]