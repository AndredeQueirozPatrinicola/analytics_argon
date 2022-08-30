# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('teste', views.testes, name='testes'),

    path('atualizadb_dep', views.popula_db_dep, name='popula_db_dep'),

    path('atualizadb/', views.popula_db, name='populadb'),

    path('deletadb', views.deleta_db, name='deleta_db'),

    path('departamentos', views.departamentos, name='departamentos'),

    path('<str:sigla>/docente/<str:parametro>', views.docente, name='docente'),

    path('<str:sigla>/docentes', views.docentes, name='docentes'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
