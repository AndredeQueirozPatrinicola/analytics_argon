import pandas as pd
import numpy as np
from datetime import datetime


from apps.home.classes.graficos import Grafico
from apps.home.models import Docente, Departamento


class Departamentos():

    def __init__(self):
        pass

    def trata_dados_ic(self, dados, anos):
        lista_todos_numeros = []
        x = 0
        for i in dados:

            y = 0
            for j in anos:

                lista_todos_numeros.append(list(i.get(j).values()))

                y += 1

            x += 1

        z = 0
        valor = z
        lista_valores_organizados = []
        x = 0
        while z <= 6:
            y = 0
            lista_passageira = []
            x = 0
            while x <= 10:
                if valor >= 66:
                    break
                lista_passageira.append(lista_todos_numeros[valor])
                valor += 6

                x += 1

            lista_valores_organizados.append(lista_passageira)
            z += 1
            valor = z

        x = 0
        resultado = {}
        while x < len(lista_valores_organizados) - 1:

            resultado[anos[x]] = list(
                np.sum(lista_valores_organizados[x], axis=0))

            x += 1

        return resultado


    def tabela_todos_docentes(self):
        dados = Docente.objects.raw(
            'SELECT id, api_docentes from home_docente;')

        departamentos_siglas = {'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Lingüística', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}

        siglas = list(departamentos_siglas.keys())

        lista_forma_df = []
        for i in dados:
            lista_forma_df.append(i.api_docentes)

        df = pd.DataFrame(lista_forma_df)
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
        dados = Docente.objects.raw(
            "SELECT id, api_docentes FROM analytics.home_docente hd ;")

        dados = [i.api_docentes for i in dados]

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

        grafico = grafico.grafico_pizza(values=valores_cursos, names=nomes_cursos, margin=dict(l=10, r=10, t=10, b=5), x=0.5, y=-0.5, color=df2.index, height=700,
                                        color_discrete_sequence=["#052e70", '#1a448a', '#264a87', '#425e8f', '#667691', '#7585a1', '#7d8da8', "#9facc2", "#91a8cf", "#AFAFAF", "#d4d4d4"])

        return grafico, titulo

    def grafico_bolsa_sem(self):
        dados = Departamento.objects.raw(
            "SELECT id, api_pesquisa_parametros FROM analytics.home_departamento hd;")

        dados = [i.api_pesquisa_parametros[0] for i in dados]

        anos = [str(i) for i in range(
            (datetime.now().year - 6), datetime.now().year)]

        resultado = self.trata_dados_ic(dados,anos)

        df = pd.DataFrame(resultado)
        df = df.transpose()
        df = df.drop(columns=[2, 3])
        df = df.rename(columns={0: "IC's com bolsa", 1: "IC's sem bolsa",
                       4: "Pos Doutorado com bolsa", 5: "Pos Doutorado sem bolsa"})

        fig = Grafico()
        fig = fig.grafico_barras(df=df, x=[i for i in anos], y=["IC's com bolsa", "IC's sem bolsa", "Pos Doutorado com bolsa", "Pos Doutorado sem bolsa"], barmode='group', height=400, color_discrete_map={
            "IC's com bolsa": "#053787",
            "IC's sem bolsa": "#264a87",
            "Pos Doutorado com bolsa": "#9facc2",
            "Pos Doutorado sem bolsa": "#AFAFAF"},
            labels={
                'x': '',
                'variable': 'Legenda',
        }, margin=dict(
            l=0, r=30, t=20, b=50), font_color="white", legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ), bargroupgap=0, bargap=0.3, autosize=True, yaxis_title="",
            linecolor='white', gridcolor='#4d4b46')

        titulo = "IC's e Pós Doutorado com e sem bolsas"

        return fig, titulo


    def tabela_trabalhos(self):
        dados = Departamento.objects.raw(
            "SELECT id, api_pesquisa_parametros FROM analytics.home_departamento hd;")

        dados = [i.api_pesquisa_parametros[0] for i in dados]

        anos = [str(i) for i in range(
            (datetime.now().year - 6), datetime.now().year)]

        resultado = self.trata_dados_ic(dados,anos)

        df = pd.DataFrame(resultado)
        df = df.rename(index={0: "IC's com bolsa", 1: "IC's sem bolsa", 2: "Pesquisadores colaboradores ativos", 3 : "Projetos de pesquisa dos Docentes",
                       4: "Pos Doutorado com bolsa", 5: "Pos Doutorado sem bolsa"})

        
        lista_valores = df.values.tolist()

        nomes = ["IC's com bolsa", "IC's sem bolsa", "Pesquisadores colaboradores ativos", "Projetos de pesquisa dos Docentes", "Pos Doutorado com bolsa", "Pos Doutorado sem bolsa"]

        x = 0
        for i in lista_valores:

            lista_valores[x].insert(0, nomes[x])

            x += 1

        titulos = ['Titulos', '2016', '2017', '2018', '2019', '2020', '2021']

        return lista_valores, titulos


    def prod_todos_departamentos(self):

        dados = Departamento.objects.all().values('api_programas_docente')

        print(dados)



