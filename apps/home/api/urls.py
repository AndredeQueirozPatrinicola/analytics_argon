from django.urls import path, include
from apps.home import views

from rest_framework import routers

from .views import GraficoRacaAPIView, GraficoSexoAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('graduacao/raca-por-ano', GraficoRacaAPIView.as_view(), name='graduacao'),
    path('graduacao/raca-por-ano/<str:graduacao>', GraficoRacaAPIView.as_view(), name='graduacao'),

    path('graduacao/sexo-por-ano', GraficoSexoAPIView.as_view(), name='sexo'),
    path('graduacao/sexo-por-ano/<str:graduacao>', GraficoSexoAPIView.as_view(), name='sexo'),
]