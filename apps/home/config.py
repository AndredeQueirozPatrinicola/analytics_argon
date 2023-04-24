from django.apps import AppConfig
import requests
from datetime import datetime

def get_submenu_graduacao():
    return [
        {
            'text' : 'Geral',
            'url' : 'geral',
        },
        {
            'text' : "Diversidade",
            'url' : 'diversidade',
        },
        {
            'text' : "Pesquisa",
            'url' : 'pesquisa',
        }
    ]

def config(request):
    date = datetime.now().date()
    date = datetime.strptime(str(date), "%Y-%m-%d").strftime("%d/%m/%Y")
    api = requests.get('https://dados.fflch.usp.br/api/programas')
    dados = api.json()

    submenu_graduacao = get_submenu_graduacao()

    return  {
                'menu':[
                            {
                                'text': 'Departamentos',
                                'url': 'departamentos'
                            },
                            {
                                'text': 'Graduação',
                                'url': 'graduacao',
                                'submenu' : submenu_graduacao
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
