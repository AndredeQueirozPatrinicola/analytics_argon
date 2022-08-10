import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot


# Constantes

API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'
API_DOCENTES = API + 'docentes'
API_PROGRAMAS_DOCENTE = API_PROGRAMAS + 'docente/'


class Docente():

    def __init__(self, parametro, sigla):
        self.parametro = parametro
        res = requests.get(url=API_PROGRAMAS_DOCENTE + self.parametro)
        dados = res.json()
        self.dados = dados
        self.sigla = sigla

    def pega_caminho(self):
        res = requests.get(url=API_PROGRAMAS)
        dados = res.json()

        for i in dados['departamentos']:
            if i['sigla'] == self.sigla:
                self.nome_departamento = i['nome']

        caminho = [
            {
                'text': self.nome_departamento,
                'url': "/" + self.sigla + "/docentes"
            },
            {
                'text': self.dados.get('nome'),
                'url': '#'
            }
        ]

        return caminho

    def plota_grafico_historico_artigos(self):
        dados = self.dados
        artigos = dados.get('artigos')
        df_artigos = pd.DataFrame(artigos)
        ano = df_artigos['ANO'].value_counts()
        ano_sortado = ano.sort_index(ascending=True)
        df = pd.DataFrame(ano_sortado)

        anos = {}

        for i in range(int(df.index[0]), int(datetime.now().year) + 1):

            try:
                anos[str(i)] = list(df.loc[(str(i))])[0]
            except:
                anos[str(i)] = 0

        df = pd.DataFrame.from_dict(anos, orient='index')
        eixo_x = df.index

        linhas = px.line(df, x=eixo_x, y=0, height=390, labels={
            'index': '',
            '0': ''
        })
        linhas.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        }, margin=dict(
            l=0, r=30, t=20, b=50), font_color="white", showlegend=False)

        linhas.update_layout(autosize=True)
        linhas.update_xaxes(showline=True, linewidth=1, linecolor='white',
                            mirror=True, showgrid=True, gridwidth=1, gridcolor='grey', automargin=True)
        linhas.update_yaxes(showline=True, linewidth=1, linecolor='white',
                            mirror=True, showgrid=True, gridwidth=1, gridcolor='grey', automargin=True)

        graph = plot(linhas, output_type="div", config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        grafico_titulo = {
            'titulo': 'Produção de artigos por ano (' + df.index[0] + '-' + str(datetime.now().year) + ')',
            'categoria': 'Artigos'
        }

        return graph, grafico_titulo

    def plota_grafico_historico_livros(self):
        dados = self.dados
        livros = dados.get('livros')
        df_livros = pd.DataFrame(livros)
        ano = df_livros['ANO'].value_counts()
        ano_sortado = ano.sort_index(ascending=True)
        df = pd.DataFrame(ano_sortado)

        anos = {}

        for i in range(int(df.index[0]), int(datetime.now().year) + 1):

            try:
                anos[str(i)] = list(df.loc[(str(i))])[0]
            except:
                anos[str(i)] = 0

        df = pd.DataFrame.from_dict(anos, orient='index')
        eixo_x = df.index

        linhas = px.line(df, x=eixo_x, y=0, height=390, labels={
            'index': '',
            '0': ''
        })
        linhas.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        }, margin=dict(
            l=0, r=30, t=20, b=50), font_color="white", showlegend=False)

        linhas.update_layout(autosize=True)
        linhas.update_xaxes(showline=True, linewidth=1, linecolor='white',
                            mirror=True, showgrid=True, gridwidth=1, gridcolor='grey', automargin=True)
        linhas.update_yaxes(showline=True, linewidth=1, linecolor='white',
                            mirror=True, showgrid=True, gridwidth=1, gridcolor='grey', automargin=True)

        graph = plot(linhas, output_type="div", config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        grafico_titulo = {
            'titulo': 'Produção de livros por ano (' + df.index[0] + '-' + str(datetime.now().year) + ')',
            'categoria': 'Livros'
        }

        return graph, grafico_titulo

    def plota_grafico_historico(self):
        dados = self.dados
        graficos = [{'nome_api': 'artigos', 'value_counts': 'ANO', 'nome_grafico': 'Artigos'}, 
                    {'nome_api': 'livros','value_counts': 'ANO', 'nome_grafico': 'Livros'}, 
                    {'nome_api': 'capitulos', 'value_counts': 'ANO', 'nome_grafico': 'Capítulos de Livros'},
                    {'nome_api' : 'jornal_revista', 'value_counts' : 'ANO', 'nome_grafico' : 'Publicações em Jornal/Revista'}]

        graficos_list = []

        for item in graficos:

            grafico_item = {}
        
            tipo_grafico = dados.get(item['nome_api'])
            df_tipo_grafico = pd.DataFrame(tipo_grafico)
            value_counts = df_tipo_grafico[item['value_counts']].value_counts()
            value_counts_organizado = value_counts.sort_index(ascending=True)
            df = pd.DataFrame(value_counts_organizado)

            print(item['nome_api'])

            value_counts_dict = {}

            for i in range(int(df.index[0]), int(datetime.now().year) + 1):

                try:
                    value_counts_dict[str(i)] = list(df.loc[(str(i))])[0]
                except:
                    value_counts_dict[str(i)] = 0

            df = pd.DataFrame.from_dict(value_counts_dict, orient='index')
            eixo_x = df.index

            fig = px.line(df, x=eixo_x, y=0, height=390, labels={
                'index': '',
                '0': ''
            })
            fig.update_layout({
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            }, margin=dict(
                l=0, r=30, t=20, b=50), font_color="white", showlegend=False)

            fig.update_layout(autosize=True)
            fig.update_xaxes(showline=True, linewidth=1, linecolor='white',
                                mirror=True, showgrid=True, gridwidth=1, gridcolor='grey', automargin=True)
            fig.update_yaxes(showline=True, linewidth=1, linecolor='white',
                                mirror=True, showgrid=True, gridwidth=1, gridcolor='grey', automargin=True)

            grafico_item['graph'] = plot(fig, output_type="div", config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

            grafico_item['grafico_titulo'] = {
                'titulo': 'Produção de livros por ano (' + df.index[0] + '-' + str(datetime.now().year) + ')',
                'categoria': item['nome_grafico'],
                'nome' : item['nome_api']
            }

            graficos_list.append(grafico_item)

        return graficos_list

    def plota_pizza(self):
        dados = self.dados
        if dados['orientandos']:
            df = pd.DataFrame(dados['orientandos'])

            nivpgm = list(df['nivpgm'])
            tipos = ['ME', 'DO']

            nivel = []
            x, y = 0, 0
            for i in nivpgm:
                if i == 'ME':
                    x += 1
                if i == 'DO':
                    y += 1

            nivel.append(x)
            nivel.append(y)

            figura = px.pie(values=nivel, names=tipos,  color=tipos, color_discrete_sequence=["#052e70", "#AFAFAF"], labels={
                'values': 'Valor',
                'names': 'Tipo',
                'color': 'Cor'
            })

            figura.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
                l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

            grafico_pizza = plot(figura, output_type='div', config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

            return grafico_pizza
        else:
            return None

    def tabela_orientandos(self):
        dados = self.dados
        if dados['orientandos']:
            df = pd.DataFrame(dados['orientandos'])

            nomep = list(df['nompes'])
            nivpgm = list(df['nivpgm'])
            nomare = list(df['nomare'])

            lis = []
            x = 0
            while x < len(nomep):
                lis.append([f'{nomep[x]}', f'{nivpgm[x]}', f'{nomare[x]}'])
                x += 1

            return lis
        else:
            return None

    def tabela_ultimas_publicacoes(self):
        dados = self.dados
        if dados['livros']:
            tabela = pd.DataFrame(dados['livros'])
            publicacoes = tabela.head(5)
            titulo_ano = publicacoes[['TITULO-DO-LIVRO', 'ANO']]
            publicacao_com_ano = titulo_ano.values.tolist()
            return publicacao_com_ano
        else:
            return None


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
