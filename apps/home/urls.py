# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('docentes/<str:parametro>', views.docentes, name='docentes'),

    path('departamento/<str:sigla>', views.departamento, name='departamento'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
