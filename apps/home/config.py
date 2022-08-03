# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.apps import AppConfig


def config(request):
    return {'menu':[{
                'text' : 'Programas',
                'url' : '/programas/'
            },
            {
                'text' : 'Docentes',
                'url' : '/docentes/'
            }],
            'logo' : 'brand/logo.png',
            'icon' : 'icons/fflch_simbolo.jpg',
            'name_app' : 'FFLCH | Analytics'
            }


class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'apps_home'



