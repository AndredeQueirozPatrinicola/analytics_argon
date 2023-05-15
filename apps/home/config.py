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

def get_submenu_posgraduacao():
    return [
        {
            'text' : 'Geral',
            'url' : 'geral',
        },
        {
            'text' : "Diversidade",
            'url' : 'diversidade',
        }
    ]

def config(request):
    date = datetime.now().date()
    date = datetime.strptime(str(date), "%Y-%m-%d").strftime("%d/%m/%Y")
    api = requests.get('https://dados.fflch.usp.br/api/programas')
    dados = api.json()

    ano_minimo = 2013
    ano_maximo = datetime.now().year
    anos = [i for i in range(ano_minimo, int(ano_maximo) + 1)]
    anos_reverse = list(reversed(anos))

    submenu_graduacao = get_submenu_graduacao()
    submenu_posgraduacao = get_submenu_posgraduacao()

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
                            },
                            {
                                'text' : 'Pós-Graduação',
                                'url' : 'pos-graduacao',
                                'submenu' : submenu_posgraduacao
                            }
                        ],
                'logo': 'brand/logo.png',
                'icon': 'icons/fflch_simbolo.jpg',
                'name_app': 'FFLCH | Analytics',
                'departamentos': dados['departamentos'],
                'date' : f'{date}',
                "ano_minimo" : ano_minimo,
                "ano_maximo" : ano_maximo,
                "anos" : anos,
                "anos_reverse" : anos_reverse
            }


class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'apps_home'
