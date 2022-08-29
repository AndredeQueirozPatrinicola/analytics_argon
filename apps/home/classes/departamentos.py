from unicodedata import name
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

from .apis import Api


class Departamentos():

    def __init__(self):
        pass

    def tabela_todos_docentes(self):
        api = Api()
        dados = api.pega_dados_docentes()
        #dados_programas = api.pega_dados_programas_docentes()

        df = pd.DataFrame(dados)
        df = df.drop(columns=['codset'])
        #df2 = pd.DataFrame(dados_programas['departamentos'])

        #x = 0
        #siglas_codigos = {}
       # while x < 11:
        #    siglas_codigos[df2.iloc[x]['sigla']] = df2.iloc[x]['codigo']

        #    x += 1

        #lista_valores = df.values.tolist()

        titulo = 'Todos os docentes da faculdade'
        return df, titulo

    def plota_relacao_cursos(self):
        res = requests.get('https://dados.fflch.usp.br/api/docentes')
        dados = res.json()
        df = pd.DataFrame(dados)
        valores_cursos = df['nomset'].value_counts().to_list()
        df2 = pd.DataFrame(df['nomset'].value_counts())

        x = 0
        nomes_cursos = []
        while x < len(df2):
            nomes_cursos.append(df2.index[x])
            x += 1

        fig = px.pie(values=valores_cursos, names=nomes_cursos, color=df2.index,
                     color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"])

        fig.update_layout(legend=dict(y=0.5))
        
        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=20, r=20, t=20, b=20), legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=1))
        grafico_pizza = plot(fig, output_type='div', config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = 'Relação entre tipos de vínculo de docente'


        return grafico_pizza, titulo
