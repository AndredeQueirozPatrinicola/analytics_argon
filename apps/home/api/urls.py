from django.urls import path, include
from apps.home import views

from rest_framework import routers

from .graficos import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

    ##########################################
    ##               GRAFICOS               ##
    ##########################################

    path('graduacao/raca-por-ano', GraficoRacaAPIView.as_view(), name='raca'),
    path('graduacao/raca-por-ano/<str:graduacao>', GraficoRacaAPIView.as_view(), name='raca'),

    path('graduacao/sexo-por-ano', GraficoSexoAPIView.as_view(), name='sexo'),
    path('graduacao/sexo-por-ano/<str:graduacao>', GraficoSexoAPIView.as_view(), name='sexo'),

    path('graduacao/sexo-atual', GraficoPizzaSexo.as_view(), name='sexo-atual'),
    path('graduacao/sexo-atual/<str:graduacao>', GraficoPizzaSexo.as_view(), name='sexo-atual'),

    path('graduacao/raca-atual', GraficoPizzaRaca.as_view(), name='raca-atual'),
    path('graduacao/raca-atual/<str:graduacao>', GraficoPizzaRaca.as_view(), name='raca-atual'),

    path('departamentos/prod-por-ano', GraficoProducaoHistoricaDepartamentos.as_view(), name='prod-por-ano'),
    path('departamentos/prod-por-ano/<str:departamento>', GraficoProducaoHistoricaDepartamentos.as_view(), name='prod-por-ano'),

    path('departamentos/prod-total', GraficoProducaoDepartamentos.as_view(), name='prod-total'),
    path('departamentos/prod-total/<str:departamento>', GraficoProducaoDepartamentos.as_view(), name='prod-total'),

    path('departamentos/ic-bolsa-sem', GraficoBolsaSemICePosDoc.as_view(), name='ic-bolsa-sem'),
    path('departamentos/ic-bolsa-sem/<str:departamento>', GraficoBolsaSemICePosDoc.as_view(), name='ic-bolsa-sem'),

    path('departamentos/defesas', GraficoDefesasDepartamentos.as_view(), name='defesas'),
    path('departamentos/defesas/<str:departamento>', GraficoDefesasDepartamentos.as_view(), name='defesas'),

    path('departamentos/professores', GraficoDocentesNosDepartamentos.as_view(), name='professores-proporcoes'),

    path('departamentos/tipo-vinculo', GraficoTipoVinculo.as_view(), name='tipo-vinculo'),
    path('departamentos/tipo-vinculo/<str:departamento>', GraficoTipoVinculo.as_view(), name='tipo-vinculo'),


    ##########################################
    ##              TABELAS                 ##
    ##########################################

    ]