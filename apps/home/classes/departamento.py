from unicodedata import name
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

from .apis import Api

from apps.home.models import Departamento



class DadosDepartamento():

    def __init__(self, sigla):
        self.sigla = sigla

    def tabela_docentes(self, sigla):
        api_programas = Departamento.objects.filter(sigla=sigla).values_list('api_programas')
        api_docentes = Departamento.objects.filter(sigla=sigla).values_list('api_docentes')

        dados_programas = api_programas[0][0]
        dados_docentes = api_docentes[0][0]

        for i in dados_programas:
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
        api = Departamento.objects.filter(sigla=sigla).values_list('api_programas')
        dados = api[0][0]

        docentes, x, y, z = self.tabela_docentes(sigla)
        df = pd.DataFrame(dados)

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
        api = Departamento.objects.filter(sigla=sigla).values_list('api_docentes')
        dados = api
        dados = dados[0][0]
        
        x = 0
        nomefnc = []
        while x < len(dados):
            nomefnc.append(dados[x].get('nomefnc'))
            
            x += 1

        df = pd.DataFrame(nomefnc)

        lista_nomes = df.value_counts().index.to_list()
        nomes = [i[0] for i in lista_nomes]

        lista_valores = df.value_counts().to_list()


        fig = px.pie(values=lista_valores, names=nomes, color=nomes,
                     color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"])
        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        grafico_pizza = plot(fig, output_type='div', config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        titulo = 'Relação entre tipos de vínculo de docente'

        return grafico_pizza, titulo

    def plota_prod_departamento(self, sigla):
        api = Departamento.objects.filter(sigla=sigla).values_list('api_programas_docente_limpo')
        dados = api[0][0]
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
        api = Departamento.objects.filter(sigla=sigla).values_list('api_pesquisa')
        dados = api[0][0]

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
        api = Departamento.objects.filter(sigla=self.sigla).values_list('api_pesquisa_parametros')
        dados = api[0][0]
        
        df = pd.DataFrame(dados[0])
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
        #api = Api()
        #dados = api.pega_dados_programas_docentes(sigla)
        api = Departamento.objects.filter(sigla=sigla).values_list('api_programas_docente')
        dados = api[0][0]
        anos = [ '2016','2017', '2018', '2019', '2020', '2021']
        anos_int = [2016, 2017, 2018, 2019, 2020, 2021]

        lista_livros = []
        lista_artigos = []
        lista_capitulos = []
        x = 0
        while x < len(anos):    
            
            z = 0
            while z < len(dados[x].get(anos[x])):
                lista_livros.append(dados[x].get(anos[x])[z].get('total_livros'))
                lista_artigos.append(dados[x].get(anos[x])[z].get('total_artigos'))
                lista_capitulos.append(dados[x].get(anos[x])[z].get('total_capitulos'))
            
                z += 1
            
            x += 1


            
        lista_livros = [int(i) for i in lista_livros]
        lista_artigos = [int(i) for i in lista_artigos]
        lista_capitulos = [int(i) for i in lista_capitulos]
            
            
        resultado_livros = []
        resultado_artigos = []
        resultado_capitulos = []

        g = 0
        f = len(dados[0].get('2016'))

        while f < len(lista_livros) + len(dados[0].get('2016')):
            
            resultado_livros.append(sum(lista_livros[g:f]))
            resultado_artigos.append(sum(lista_artigos[g:f]))
            resultado_capitulos.append(sum(lista_capitulos[g:f]))
            
            g = f
            f += len(dados[0].get('2016'))
            
            
        resultado = {}
        s = 0
        while s < len(anos_int):
            
            resultado[anos_int[s]] = {
                'total_livros' : resultado_livros[s],
                'total_artigos' : resultado_artigos[s],
                'total_capitulos' : resultado_capitulos[s]
            }
            
            s += 1
            
        df = pd.DataFrame(resultado)
        df = df.transpose()
        df = df.rename(columns = {'total_livros' : 'Livros', 'total_artigos' : 'Artigos', 'total_capitulos' : 'Capitulos'})
        fig = px.histogram(df, x=['2016', '2017', '2018', '2019', '2020', '2021'], y=['Livros','Artigos','Capitulos'], height=478, barmode = 'group', color_discrete_map={
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


