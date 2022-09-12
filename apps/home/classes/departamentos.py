import pandas as pd
import requests
from datetime import datetime

from .apis import Api

from apps.home.classes.graficos import Grafico


class Departamentos():

    def __init__(self):
        pass

    def tabela_todos_docentes(self):
        api = Api()
        dados = api.pega_dados_docentes()

        departamentos_siglas = {'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Lingüística', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}

        siglas = list(departamentos_siglas.keys())

        df = pd.DataFrame(dados)
        df = df.drop(columns=['codset'])

        lista_siglas = []
        for i in df['nomset']:
            for j in siglas:
                if i == departamentos_siglas.get(j):
                    lista_siglas.append(j)

        df['sigset'] = lista_siglas

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

        titulo = 'Percentual de professores por departamento'

        grafico = Grafico()

        grafico = grafico.grafico_pizza(values=valores_cursos, names=nomes_cursos,margin=dict(l=10,r=10,t=10,b=5),x=0.5, y=-0.5 ,color=df2.index, height=700,
                                        color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF", '#0958D9', '#4C84DF', "#0744A6", "#090fba", "#216fcf"])

        return grafico, titulo


