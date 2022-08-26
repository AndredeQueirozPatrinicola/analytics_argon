from unicodedata import name
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

from .apis import Api

API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'
API_DOCENTES = API + 'docentes'
API_PROGRAMAS_DOCENTE = API_PROGRAMAS + 'docentes/'
API_PESQUISA = API + 'pesquisa'


class Departamento():

    def __init__(self, sigla):
        self.sigla = sigla

    def tabela_docentes(self, sigla):
        api = Api()
        dados = api.pega_dados_programas()
        dados_docentes = api.pega_dados_docentes()

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
        api = Api()
        dados = api.pega_dados_programas()
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
        api = Api()
        dados = api.pega_dados_docentes()

        departamentos_siglas = {'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Lingüística', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}

        df = pd.DataFrame(dados)
        df = df[['nomset', 'nomefnc']]
        df = df.loc[df['nomset'] == departamentos_siglas.get(sigla)]

        var = df['nomefnc'].value_counts()
        df2 = pd.DataFrame(var)

        fig = px.pie(df2, values='nomefnc', names=df2.index, color=df2.index,
                     color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"])
        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        grafico_pizza = plot(fig, output_type='div', config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = 'Relação entre tipos de vínculo de docente'

        return grafico_pizza, titulo

    def plota_prod_departamento(self, sigla):
        api = Api()
        dados = api.pega_dados_programas_docentes(sigla)

        df = pd.DataFrame(dados)
        somas = df['total_livros'].to_list(
        ), df['total_artigos'].to_list(), df['total_capitulos'].to_list()

        x = 0
        lista_valores = []
        while x < len(somas):
            lista_valores_individuais = [int(i) for i in somas[x]]
            lista_valores.append(sum(lista_valores_individuais))
            x += 1

        fig = px.bar(x=['Total de livros', 'Total de artigos', 'Total de capitulos'], y=lista_valores, color=['Total de livros', 'Total de artigos', 'Total de capitulos'],
                     color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"])

        fig.update_yaxes(title='', showticklabels=True, showline=True, linewidth=1, linecolor='#e0dfda',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#e0dfda', automargin=True)
        fig.update_xaxes(title='', showticklabels=True, showline=True, linewidth=1, linecolor='#e0dfda',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#e0dfda', automargin=True)

        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=15, r=15, t=15, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), showlegend=False)

        grafico = plot(fig, output_type='div', config={
            'displaylogo': False,
            'displayModeBar': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = 'Produção total do departamento'

        return grafico, titulo

    def tabela_trabalhos(self, sigla):

        api = Api()
        dados = api.pega_dados_pesquisa()

        df = pd.DataFrame(dados)
        df2 = pd.DataFrame(df[sigla])
        df2 = df2.rename(index={
                        'nome_departamento': "Nome do departamento", 
                        'ic_com_bolsa': "IC com bolsa",
                        'ic_sem_bolsa': "IC sem bolsa",
                        'pesquisadores_colab': 'Pesquisadores colaboradores ativos',
                        'projetos_pesquisa': 'Projetos de pesquisa dos Docentes',
                        'pesquisas_pos_doutorado_com_bolsa': 'Pesquisas pós doutorado com bolsa', 
                        'pesquisas_pos_doutorado_sem_bolsa': 'Pesquisas pós doutorado sem bolsa'
                        })
        indices = df2.index
        indices.to_list()
        valores = df2[sigla].to_list()

        x = 0
        dic = []
        while x < len(indices):
            tabela_dados = [indices[x], valores[x]]
            dic.append(tabela_dados)
            x += 1

        return dic

    def plota_grafico_bolsa_sem(self):

        api = Api()
        dados = api.pega_dados_pesquisa('serie_historica', 2016, 2021, 'departamento')

        departamentos_siglas = {'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Linguística', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}

        df = pd.DataFrame(dados[departamentos_siglas.get(self.sigla)])
        df = df.drop(['pesquisadores_colab'])
        df = df.transpose()
        df = df.rename(columns={
                                "ic_com_bolsa": "IC com bolsa", 
                                "ic_sem_bolsa": "IC sem bolsa", 
                                'pesquisas_pos_doutorado_com_bolsa':'Pesquisas pós doutorado com bolsa', 
                                'pesquisas_pos_doutorado_sem_bolsa': 'Pesquisas pós doutorado sem bolsa'
                                })
        fig = px.histogram(df, x=['2016', '2017', '2018', '2019', '2020', '2021'], y=['IC com bolsa', 'IC sem bolsa','Pesquisas pós doutorado com bolsa', 'Pesquisas pós doutorado sem bolsa'], 
        barmode='group', height=400, color_discrete_map={
            "IC com bolsa": "#053787",
            "IC sem bolsa": "#264a87",
            "Pesquisas pós doutorado com bolsa": "#9facc2",
            "Pesquisas pós doutorado sem bolsa": "#AFAFAF"}, 
            labels={
                'x': '',
                'variable': 'Legenda',
            })

        fig.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        }, margin=dict(
            l=0, r=30, t=20, b=50), font_color="white", legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ), bargroupgap=0, bargap=0.3, autosize=True, yaxis_title="")

        fig.update_xaxes(showline=True, linewidth=1, linecolor='white',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#4d4b46', automargin=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#4d4b46', automargin=True)

        grafico = plot(fig, output_type='div', config={
            'displaylogo': False,
            'displayModeBar': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = "Relação entre IC's e Pesquisas de pós com e sem bolsa - (2016-2021)"

        return grafico, titulo


    
    def plota_prod_serie_historica(self, sigla):
        api = Api()
        dados = api.pega_dados_programas_docentes(sigla)

        anos = [2016,2017,2018,2019,2020,2021]
    
        resultados = []
        y = 0
        while y < len(anos):
        
            parametros = {
                'tipo':'anual',
                'ano' : anos[y],
                'ano_ini' : '',
                'ano_fim' : ''
            }

            api = requests.get(url = f'https://dados.fflch.usp.br/api/programas/docentes/{sigla}', params = parametros)

            dados = api.json()

            df = pd.DataFrame(dados)

            somas = df['total_livros'].to_list(
            ), df['total_artigos'].to_list(), df['total_capitulos'].to_list()

            x = 0
            lista_valores = []
            while x < len(somas):
                lista_valores_individuais = [int(i) for i in somas[x]]
                lista_valores.append(sum(lista_valores_individuais))
                x += 1
                
            resultados.append(lista_valores)
            
            y += 1


        df2 = pd.DataFrame(resultados, anos)
        df2 = df2.rename(columns = {0 : 'Livros', 1 : 'Artigos', 2 : 'Capitulos'})

        fig = px.histogram(df2, x=['2016', '2017', '2018', '2019', '2020', '2021'], y=['Livros', 'Artigos', 'Capitulos'], height=478, barmode = 'group', color_discrete_map={
            "Livros": "#053787",
            "Artigos": "#9facc2",
            "Capitulos": "#AFAFAF"
            }, 
            labels={
                'x': '',
                'variable': 'Legenda',
            })

        fig.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        }, margin=dict(
            l=0, r=30, t=20, b=50), font_color="black", legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ), bargroupgap=0, bargap=0.3, autosize=True, yaxis_title="")

        fig.update_xaxes(showline=True, linewidth=1, linecolor='#e0dfda',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#e0dfda', automargin=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='#e0dfda',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#e0dfda', automargin=True)

        grafico = plot(fig, output_type='div', config={
            'displaylogo': False,
            'displayModeBar': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = "Produção do departamento - (2016-2021)"

        return grafico, titulo