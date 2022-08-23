from unicodedata import name
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'
API_DOCENTES = API + 'docentes'
API_PROGRAMAS_DOCENTE = API_PROGRAMAS + 'docente/'


class Departamento():

    def __init__(self, sigla):
        res = requests.get(url=API_PROGRAMAS)
        dados = res.json()
        res_docentes = requests.get(url=API_DOCENTES)
        dados_docentes = res_docentes.json()
        self.dados_docentes = dados_docentes
        self.dados = dados
        self.sigla = sigla

    def tabela_docentes(self, sigla):
        dados = self.dados
        dados_docentes = self.dados_docentes

        for i in dados['departamentos']:
            if i['sigla'] == sigla:
                nome = i['nome']
                id = i['id_lattes_docentes']
                codset = i['codigo']

        docentes = [i for i in dados_docentes if int(
            i['codset']) == int(codset)]

        df = pd.DataFrame(docentes)

        id_lattes = df['id_lattes']

        return df, id_lattes, nome, id

    def pega_numero_docentes(self, sigla):
        dados = self.dados
        docentes, x, y, z = self.tabela_docentes(sigla)
        df = pd.DataFrame(dados['departamentos'])

        valor = df['sigla'].to_list().index(sigla)
        resultado = df['total_docentes'].iloc[valor]

        aposentados = len(docentes) - resultado

        conteudo = {
            'texto_ativos': 'Numero de docentes(ativos): ',
            'numero_ativos': resultado,
            'texto_aposentados': 'Numero de docentes(aposentados): ',
            'numero_aposentados': aposentados
        }

        return conteudo

    def plota_aposentados_ativos(self, sigla):
        dados = self.pega_numero_docentes(sigla)

        ativos_aposentados = [
            dados.get('numero_ativos'), dados.get('numero_aposentados')]
        tipos = ['Ativos', "Aposentados"]

        titulo = 'Relação entre aposentados e ativos'

        fig = px.pie(values=ativos_aposentados, names=tipos,
                     color=tipos, color_discrete_sequence=["#052e70", "#AFAFAF"])

        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

        grafico_pizza = plot(fig, output_type='div', config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        return grafico_pizza, titulo

    def plota_tipo_vinculo_docente(self, sigla):
        dados = self.dados_docentes

        departamentos_siglas = {'FLA': 'Antrolopogia', 'FLP': 'Ciência Politica', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Linguistica', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}

        print(departamentos_siglas.get(sigla))

        df = pd.DataFrame(dados)
        df = df[['nomset', 'nomefnc']]
        df = df.loc[df['nomset'] == departamentos_siglas.get(sigla)]
        var = df['nomefnc'].value_counts()
        df2 = pd.DataFrame(var)

        fig = px.pie(df2, values='nomefnc', names=df2.index, color=df2.index,
                     color_discrete_sequence=["#052e70", '#264a87', '#667691', "#AFAFAF"])
        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        grafico_pizza = plot(fig, output_type='div', config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = 'Relação entre tipos de vínculo de docente'

        return grafico_pizza, titulo
