from django.urls import path, include
from apps.home import views

from rest_framework import routers

from .views import GraficoRacaAPIView, GraficoSexoAPIView, GraficoPizzaSexo, GraficoPizzaRaca, GraficoProducaoHistoricaDepartamentos

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('graduacao/raca-por-ano', GraficoRacaAPIView.as_view(), name='raca'),
    path('graduacao/raca-por-ano/<str:graduacao>', GraficoRacaAPIView.as_view(), name='raca'),

    path('graduacao/sexo-por-ano', GraficoSexoAPIView.as_view(), name='sexo'),
    path('graduacao/sexo-por-ano/<str:graduacao>', GraficoSexoAPIView.as_view(), name='sexo'),

    path('graduacao/sexo-atual', GraficoPizzaSexo.as_view(), name='sexo-atual'),
    path('graduacao/sexo-atual/<str:graduacao>', GraficoPizzaSexo.as_view(), name='sexo-atual'),

    path('graduacao/raca-atual', GraficoPizzaRaca.as_view(), name='raca-atual'),
    path('graduacao/raca-atual/<str:graduacao>', GraficoPizzaRaca.as_view(), name='raca-atual'),

    path('departamentos/prod-por-ano', GraficoProducaoHistoricaDepartamentos.as_view(), name='prod-por-ano'),
    path('departamentos/prod-por-ano/<str:departamento>', GraficoProducaoHistoricaDepartamentos.as_view(), name='prod-por-ano')
]