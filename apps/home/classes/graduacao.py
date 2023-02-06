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
            'titulo' : 'Numero de Alunos Ativos',
            'text' : dados[0][0]
        }
        return resultado

    def pega_dados_raca(self):
        if self.graduacao:
            dados = self.etl.pega_dados_por_ano("raca", order_by='raca', where=self.graduacao)
        else:
            dados = self.etl.pega_dados_por_ano("raca", order_by='raca')
            
        df = pd.DataFrame(dados)
        df = df.rename(columns={
                                    1:self.etl.anos[0], 
                                    2:self.etl.anos[1],
                                    3:self.etl.anos[2], 
                                    4:self.etl.anos[3], 
                                    5:self.etl.anos[4],
                                    6:self.etl.anos[5],
                                    7:self.etl.anos[6]
                                })
        resultado = []
        for ano in range(1, 8):
            ano_nome = str(ano + 2016)
            ano_dados = {}
            for row in df.itertuples(index=False):
                ano_dados[row[0]] = row[ano]
            resultado.append({'ano': ano_nome, 'dados': ano_dados})
        return resultado

    def trata_dados_raca_api(self, type, labels, colors):
        api = self.pega_dados_raca()

        datasets = []
        for i in range(len(labels)):
            data = []
            for j in range(len(api)):
                label = labels[i]
                data.append(api[j]["dados"][label])
            datasets.append(
                {
                    "label": labels[i],
                    "data": data,
                    "backgroundColor": colors[i],
                    "borderWidth": 1,
                }
            )
        result = {
            'type' : type,
            'data' : {
                'labels' : self.etl.anos,
                'datasets' : datasets
            },
            'responsive' : True,
        }
        return result



