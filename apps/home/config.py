from django.apps import AppConfig
import requests
from datetime import datetime

def config(request):
    date = datetime.now().date()
    date = datetime.strptime(str(date), "%Y-%m-%d").strftime("%d/%m/%Y")
    api = requests.get('https://dados.fflch.usp.br/api/programas')
    dados = api.json()

    menu_departamentos = [{'text': 'Geral', 'url': '/departamentos'}]

    for i in dados['departamentos']:

        nome = i['nome']

        menu_departamentos.append({
            'text': nome,
            'url': '/departamentos/' + i['sigla']
        })

    return  {
                'menu':[
                        {
                            'text': 'Departamentos',
                            'url': '/departamentos/',
                            'submenu': menu_departamentos
                        },
                        {
                            'text': 'Graduação',
                            'url': '/graduacao/',
                        }
                        ],
                'logo': 'brand/logo.png',
                'icon': 'icons/fflch_simbolo.jpg',
                'name_app': 'FFLCH | Analytics',
                'departamentos': dados['departamentos'],
                'date' : f'{date}'
            }


class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'apps_home'
