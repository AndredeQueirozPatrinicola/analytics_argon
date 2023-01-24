import pandas as pd
import numpy as np
from datetime import datetime

from django.db import connections

from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils


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

    def grafico_diversidade(self):
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        data = f"{dia}/{mes}/{ano}"

        self.cursor.execute(f"""
                            SELECT 
                                ag.raca,
                                ag.sexo,
                                COUNT(*)
                            FROM alunos_graduacao ag 
                            JOIN graduacoes g 
                                ON ag.numeroUSP = g.numeroUSP 
                            WHERE g.situacao = 'Ativo'
                            GROUP BY 
                                ag.raca, ag.sexo 
                            ORDER BY 
                                COUNT(*) DESC  ;
                            """)

        df = self.cursor.fetchall()
        df = pd.DataFrame(df)

        grafico = Grafico()
        grafico = grafico.grafico_barras(df=df, x=0, y=2, height=478, barmode='group', 
                                            color_discrete_sequence=["#053787","#9facc2"]
                                            , labels={
                                                'x' : '',
                                                'variable' : 'Legenda',
                                                'value' : 'Valor'
                                            },
                                            margin=dict(
                                                l=0, r=30, t=20, b=50), font_color="black", legend=dict(
                                                yanchor="top",
                                                y=0.99,
                                                xanchor="right",
                                                x=0.99
                                            ), bargroupgap=0, bargap=0.3, autosize=True, yaxis_title="",
                                            linecolor='#e0dfda', gridcolor='#e0dfda')

        titulo = f"Diversidade de sexo e raça dos alunos de graduação com vínculo ativo({data})."

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico 
        }

        return resultado

