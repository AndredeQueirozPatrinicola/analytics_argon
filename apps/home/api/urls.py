from django.urls import path, include, re_path
from apps.home import views

from rest_framework import routers

from .graficos import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

    ##########################################
    ##               GRAFICOS               ##
    ##########################################

    re_path(r'^graduacao/raca-por-ano(/(?P<graduacao>[\w\s\-]+))?$', GraficoRacaAPIView.as_view(), name='raca'),

    re_path(r'^graduacao/sexo-por-ano(/(?P<graduacao>[\w\s\-]+))?$', GraficoSexoAPIView.as_view(), name='sexo'),

    re_path(r'^graduacao/sexo-atual(/(?P<graduacao>[\w\s\-]+))?$', GraficoPizzaSexo.as_view(), name='sexo-atual'),

    re_path(r'^graduacao/raca-atual(/(?P<graduacao>[\w\s\-]+))?$', GraficoPizzaRaca.as_view(), name='sexo-raca'),

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