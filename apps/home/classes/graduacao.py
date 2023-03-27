import pandas as pd
import numpy as np
from datetime import datetime

from django.db import connections

from apps.home.models import *
from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils
from .etl import Etl


class Graduacao:

    def __init__(self, graduacao=False) -> None:
        self.graduacao = graduacao
        self.cursor = connections['etl'].cursor()
        self.etl = Etl()
        
    def pega_caminho(self):
        return [
            {
                'text' : 'Graduação',
                'url' : '#'
            }
        ]

    def pega_numero_alunos_ativos(self):
        dados = Graduacoes.objects.using('etl').filter(situacao_curso = 'ativo')
        resultado = {
            'title' : 'Numero de Alunos Ativos',
            'text' : f"Alunos: {len(dados)}"
        }
        return resultado












