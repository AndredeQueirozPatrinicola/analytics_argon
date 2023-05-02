from django.urls import path, include, re_path
from apps.home import views

from rest_framework import routers

from .graficos import *
from .mapas import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

    path('raca-sexo', GraficoRacaSexo.as_view(), name='raca-sexo'),

    ##########################################
    ##               GRAFICOS               ##
    ##########################################

    path('raca-por-ano', GraficoRacaAPIView.as_view(), name='raca'),

    path('sexo-por-ano', GraficoSexoAPIView.as_view(), name='sexo'),

    path('sexo-atual', GraficoPizzaSexo.as_view(), name='sexo-atual'),

    path('raca-atual', GraficoPizzaRaca.as_view(), name='sexo-raca'),

    path('prod-por-ano', GraficoProducaoHistoricaDepartamentos.as_view(), name='prod-por-ano'),

    path('prod-total', GraficoProducaoDepartamentos.as_view(), name='prod-total'),

    path('defesas', GraficoDefesasDepartamentos.as_view(), name='defesas'),

    path('tipo-vinculo', GraficoTipoVinculo.as_view(), name='tipo-vinculo'),

    path('professores', GraficoDocentesNosDepartamentos.as_view(), name='professores-proporcoes'),

    path('docentes/<str:docente>/orientandos', GraficoOrientandos.as_view(), name='orientandos'),

    path('docentes/<str:docente>/producao-historica', GraficoProducaoHistoricaDocente.as_view(), name='producao-historica'),
    
    path('docentes/<str:docente>/producao-historica/<str:tipo>', GraficoProducaoHistoricaDocente.as_view(), name='producao-historica'),

    path("ingressantes-egressos", GraficoIngressantesEgressos.as_view(), name='ingressantes-egressos'),

    path("tipo-ingresso", GraficoTipoIngresso.as_view(), name="tipo-ingresso"),

    path("tipo-egresso", GraficoTipoEgresso.as_view(), name="tipo-egresso"),

    ##########################################
    ##              TABELAS                 ##
    ##########################################

    ]