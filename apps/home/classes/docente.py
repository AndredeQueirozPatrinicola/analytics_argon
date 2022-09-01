import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

from apps.home.models import Docente


API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'


class DadosDocente():

    def __init__(self, parametro, sigla):
        self.parametro = parametro
        self.sigla = sigla


    def linhas_de_pesquisa(self):
        api = Docente.objects.filter(docente_id=self.parametro).values_list()
        dados = api[0][2]
        linhas_pesquisa = dados.get('linhas_pesquisa')

        linhas_titulo = {
            'text' : "Linhas de Pesquisa",
        }


        return linhas_titulo, linhas_pesquisa


    def pega_caminho(self):
        try:
            api = Docente.objects.filter(docente_id=self.parametro).values_list()
            dados = api[0][3]
            dados_nome = api[0][2]
            self.nome_departamento = dados[0].get('nome')

        except:
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
                'text': dados_nome.get('nome'),
                'url': '#'
            }
        ]

        return caminho

    def plota_grafico_historico(self, tipo):
        try:
            api = Docente.objects.filter(docente_id=self.parametro).values_list()
            dados = api[0][2]
            livros = dados.get(tipo)
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
                                mirror=True, showgrid=True, gridwidth=1, gridcolor='#4d4b46', automargin=True)
            linhas.update_yaxes(showline=True, linewidth=1, linecolor='white',
                                mirror=True, showgrid=True, gridwidth=1, gridcolor='#4d4b46', automargin=True)

            graph = plot(linhas, output_type="div", config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})


            grafico_titulo = {
                'titulo': f'Produção de {tipo} por ano ( {df.index[0]} - {str(datetime.now().year)} )',
                'categoria': tipo
            }

            return graph, grafico_titulo
        except:
            return None, None

    def plota_grafico_pizza(self):
        api = Docente.objects.filter(docente_id=self.parametro).values_list()
        dados = api[0][2]
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
        api = Docente.objects.filter(docente_id=self.parametro).values_list()
        dados = api[0][2]
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
        api = Docente.objects.filter(docente_id=self.parametro).values_list()
        dados = api[0][2]
        if dados['livros']:
            tabela = pd.DataFrame(dados['livros'])
            publicacoes = tabela.head(5)
            titulo_ano = publicacoes[['TITULO-DO-LIVRO', 'ANO']]
            publicacao_com_ano = titulo_ano.values.tolist()
            return publicacao_com_ano
        else:
            return None


