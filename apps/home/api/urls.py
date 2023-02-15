from django.urls import path, include
from apps.home import views

from rest_framework import routers

from .views import GraficoRacaAPIView, GraficoSexoAPIView, GraficoPizzaRaca

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('graduacao/raca-por-ano', GraficoRacaAPIView.as_view(), name='raca'),
    path('graduacao/raca-por-ano/<str:graduacao>', GraficoRacaAPIView.as_view(), name='raca'),

    path('graduacao/sexo-por-ano', GraficoSexoAPIView.as_view(), name='sexo'),
    path('graduacao/sexo-por-ano/<str:graduacao>', GraficoSexoAPIView.as_view(), name='sexo'),

    path('graduacao/sexo-atual', GraficoPizzaRaca.as_view(), name='raca-atual'),
    path('graduacao/sexo-atual/<str:graduacao>', GraficoPizzaRaca.as_view(), name='raca-atual'),
]