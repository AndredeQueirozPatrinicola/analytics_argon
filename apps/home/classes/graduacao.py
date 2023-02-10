import pandas as pd
import numpy as np
from datetime import datetime

from django.db import connections

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
        dados = self.etl.conta_pessoa_por_categoria('graduacoes', 'ativo')
        resultado = {
            'title' : 'Numero de Alunos Ativos',
            'text' : f"Alunos: {dados[0][0]}"
        }
        return resultado


    def trata_dados_raca_api(self, tipo, labels, colors, departamento = False):
        if self.graduacao:
            dados = self.etl.pega_dados_por_ano("raca", order_by='raca', where=self.graduacao)
        else:
            dados = self.etl.pega_dados_por_ano("raca", order_by='raca')

        if not departamento:
            titulo = "Distribuição de todos os alunos de graduação por raça(Percentual)."
        else:
            titulo = f"DIstribuição dos alunos de {departamento.capitalize()} por raça(Percentual)."

        dados = pd.DataFrame(dados)
        dados = dados.values.tolist()

        datasets = []
        for dado in dados:
            label = dado[0]
            dado.pop(0)
            data = {
                "label" : label,
                "data" : dado,
                "backgroundColor" : colors[dados.index(dado)],
                "borderWidth" : 1
            }
            datasets.append(data)

        result = {
            'type' : tipo,
            'data' : {
                'labels' : self.etl.anos,
                'datasets' : datasets
            },
            'options': {
                'plugins' : {
                    'stacked100': { 
                        'enable': True, 
                        'replaceTooltipLabel': False 
                    },
                    'title': {
                        'display': True,
                        'text': titulo,
                        'font': {
                            'size' : 16
                        }
                    }
                }
            },
            'responsive' : True,
        }
        return result










