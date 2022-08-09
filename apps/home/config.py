# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.apps import AppConfig
import requests

def config(request):

    api = requests.get('https://dados.fflch.usp.br/api/programas')
    dados = api.json()

    menu_departamentos = [{'text': 'Geral', 'url': '/departamentos'}]

    for i in dados['departamentos']:

        menu_departamentos.append({
            'text': i['nome'],
            'url' : '/docentes/' + i['sigla'] 
            })


    return {'menu':[{
                'text' : 'Departamentos',
                'url' : '/departamentos/',
                'submenu' : menu_departamentos
            }],
            'logo' : 'brand/logo.png',
            'icon' : 'icons/fflch_simbolo.jpg',
            'name_app' : 'FFLCH | Analytics',
            'departamentos' : dados['departamentos']
            }


class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'apps_home'



