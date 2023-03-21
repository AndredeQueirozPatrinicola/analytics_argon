from django.urls import path, include, re_path
from apps.home import views

from rest_framework import routers

from .graficos import *
from .mapas import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

    path('teste', Teste.as_view(), name='teste'),

    ##########################################
    ##               GRAFICOS               ##
    ##########################################

    path('raca-por-ano', GraficoRacaAPIView.as_view(), name='raca'),

    path('sexo-por-ano', GraficoSexoAPIView.as_view(), name='sexo'),

    path('sexo-atual', GraficoPizzaSexo.as_view(), name='sexo-atual'),

    path('raca-atual', GraficoPizzaRaca.as_view(), name='sexo-raca'),

    re_path(r'^departamentos/prod-por-ano(/(?P<departamento>[\w\s\-]+))?$', GraficoProducaoHistoricaDepartamentos.as_view(), name='prod-por-ano'),

    re_path(r'^departamentos/prod-total(/(?P<departamento>[\w\s\-]+))?$', GraficoProducaoDepartamentos.as_view(), name='prod-total'),

    re_path(r'^departamentos/defesas(/(?P<departamento>[\w\s\-]+))?$', GraficoDefesasDepartamentos.as_view(), name='defesas'),

    re_path('departamentos/professores', GraficoDocentesNosDepartamentos.as_view(), name='professores-proporcoes'),

    re_path(r'^departamentos/tipo-vinculo(/(?P<departamento>[\w\s\-]+))?$', GraficoTipoVinculo.as_view(), name='tipo-vinculo'),

    re_path('docentes/<str:docente>/orientandos', GraficoOrientandos.as_view(), name='orientandos'),

    re_path('docentes/<str:docente>/producao-historica', GraficoProducaoHistoricaDocente.as_view(), name='producao-historica'),
    
    re_path('docentes/<str:docente>/producao-historica/<str:tipo>', GraficoProducaoHistoricaDocente.as_view(), name='producao-historica'),

    ##########################################
    ##              TABELAS                 ##
    ##########################################

    ]