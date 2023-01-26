import pandas as pd
import numpy as np
from datetime import datetime

from django.db import connections

from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils
from .etl import Etl


class Graduacao:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()

    def pega_caminho(self):
        return [
            {
                'text' : 'Graduação',
                'url' : '#'
            }
        ]

    def pega_numero_alunos_ativos(self):
        self.cursor.execute("""
                                SELECT COUNT(*) 
                                FROM graduacoes g 
                                WHERE situacao = 'Ativo';
                            """)

        valor = self.cursor.fetchall()
        resultado = {
            'titulo' : 'Numero de Alunos Ativos',
            'text' : valor[0][0]
        }
        return resultado

    def pega_dados_raca(self):
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        data = f"{dia}/{mes}/{ano}"

        etl = Etl()
        dados = etl.pega_dados_por_ano("raca")
        df = pd.DataFrame(dados)

        df = df.rename(columns={
                                    1:etl.anos[0], 
                                    2:etl.anos[1],
                                    3:etl.anos[2], 
                                    4:etl.anos[3], 
                                    5:etl.anos[4],
                                    6:etl.anos[5],
                                    7:etl.anos[6]
                                })

        resultado = []
        for ano in range(1, 8):
            ano_nome = str(ano + 2016)
            ano_dados = {}
            for row in df.itertuples(index=False):
                ano_dados[row[0]] = row[ano]
            resultado.append({'ano': ano_nome, 'dados': ano_dados})

        print(resultado)

        return resultado



