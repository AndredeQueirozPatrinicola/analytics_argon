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

        nome = i['nome']

        menu_departamentos.append({
            'text': nome,
            'url' : '/departamentos/' + i['sigla'] 
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



