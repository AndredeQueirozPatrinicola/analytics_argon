# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('<str:sigla>/docente/<str:parametro>', views.docente, name='docentes'),

    path('<str:sigla>/docentes', views.docentes, name='departamento'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
