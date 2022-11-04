import pandas as pd
import numpy as np
from datetime import datetime
from functools import reduce


from apps.home.classes.graficos import Grafico
from apps.home.models import Docente, Departamento
from apps.home.utils import Utils

class Departamentos():

    def __init__(self):
        pass

    def pega_numero_docentes(self):
        resultado = Docente.objects.count()
        ativo_aposentado = Docente.objects.values_list('api_docentes')

        ativo = 0
        aposentado = 0

        for i in ativo_aposentado:

            if i[0].get('sitatl') == 'A':
                ativo += 1
            elif i[0].get('sitatl') == 'P':
                aposentado += 1
           
        resultado = {
            'texto_ativos' : 'Numero de docentes',
            'numero_ativos' : { 
                                'total' : f'Total: {resultado}',
                                'ativos' : f'Ativos: {ativo}',
                                'aposentados' : f'Aposentados: {aposentado}'
                              }
            }

        return resultado

    def trata_dados_ic(self, dados, anos):
        lista_todos_numeros = []

        for i in dados:
            for j in anos:
                lista_todos_numeros.append(list(i.get(j).values()))

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
        dados = Docente.objects.raw("SELECT id, api_docentes FROM analytics.home_docente hd ;")

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

        grafico = grafico.grafico_pizza(values=valores_cursos, names=nomes_cursos, margin=dict(l=10, r=10, t=10, b=0), x=0.6, y=-0.5, color=df2.index, height=700,
                                        color_discrete_sequence=["#052e70", '#1a448a', '#264a87', '#425e8f', '#667691', '#7585a1', '#7d8da8', "#9facc2", "#91a8cf", "#AFAFAF", "#d4d4d4"])

        return grafico, titulo

    def grafico_bolsa_sem(self):
        dados = Departamento.objects.raw(
            "SELECT id, api_pesquisa_parametros FROM analytics.home_departamento hd;")

        dados = [i.api_pesquisa_parametros[0] for i in dados]

        anos = [str(i) for i in range(
            (datetime.now().year - 6), datetime.now().year)]

        resultado = self.trata_dados_ic(dados, anos)

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

        titulo = "Relação entre IC's e Pós Doutorado com e sem bolsas"

        return fig, titulo

    def tabela_trabalhos(self):
        dados = Departamento.objects.raw(
            "SELECT id, api_pesquisa_parametros FROM analytics.home_departamento hd;")

        dados = [i.api_pesquisa_parametros[0] for i in dados]

        anos = [str(i) for i in range(
            (datetime.now().year - 6), datetime.now().year)]

        resultado = self.trata_dados_ic(dados, anos)

        nomes = ["IC's com bolsa", "IC's sem bolsa", "Pesquisadores colaboradores ativos",
                 "Projetos de pesquisa dos Docentes", "Pos Doutorado com bolsa", "Pos Doutorado sem bolsa"]

        df = pd.DataFrame(resultado)
        df = df.rename(index={0: nomes[0], 1: nomes[1], 2: nomes[2], 3: nomes[2],
                       4: nomes[3], 5: nomes[4]})

        lista_valores = df.values.tolist()

        x = 0
        for i in lista_valores:

            lista_valores[x].insert(0, nomes[x])

            x += 1

        titulos = ['Titulos', '2016', '2017', '2018', '2019', '2020', '2021']

        return lista_valores, titulos

    def prod_total_departamentos(self):
        dados = Departamento.objects.values('api_programas_docente_limpo')

        x = 0
        resultado_livros = []
        resultado_artigos = []
        resultado_capitulos = []
        while x < len(dados):

            for i in range(len(dados[x].get('api_programas_docente_limpo'))):

                resultado_livros.append(dados[x].get(
                    'api_programas_docente_limpo')[i].get('total_livros'))
                resultado_artigos.append(dados[x].get('api_programas_docente_limpo')[
                                         i].get('total_artigos'))
                resultado_capitulos.append(dados[x].get('api_programas_docente_limpo')[
                                           i].get('total_capitulos'))

            x += 1

        resultado_livros = [int(i) for i in resultado_livros]
        resultado_artigos = [int(i) for i in resultado_artigos]
        resultado_capitulos = [int(i) for i in resultado_capitulos]

        resultado = [sum(resultado_livros), sum(
            resultado_artigos), sum(resultado_capitulos)]

        fig = Grafico()
        fig = fig.grafico_barras(x=['Livros', 'Artigos', 'Capitulos'], y=resultado, color=['Livros', 'Artigos', 'Capitulos'],
                                 color_discrete_sequence=[
                                     "#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"],
                                 linecolor='#e0dfda', gridcolor='#e0dfda', margin=dict(
            l=15, r=15, t=15, b=0), legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01), labels={
                                    'x': '',
                                    'color': 'Legenda'
                                    })

        titulo = 'Produção total de Artigos, Livros e Capitulos de todos os docentes da faculdade registrados no lattes'

        return fig, titulo

    def prod_historica_total(self):

        def soma_lista(a: int, b: int):
            return int(a) + int(b)

        dados = Departamento.objects.values_list('api_programas_docente')

        anos = [str(i)
                for i in range(datetime.now().year - 6, datetime.now().year)]

        tipos = ['total_livros', 'total_artigos', 'total_capitulos']

        resultado = []
        s = 0
        while s < len(tipos):

            dados_primeiro_ano = []
            dados_segundo_ano = []
            dados_terceiro_ano = []
            dados_quarto_ano = []
            dados_quinto_ano = []
            dados_sexto_ano = []
            x = 0
            while x < len(dados):

                y = 0
                while y < len(dados[x][0]):

                    z = 0
                    while z < len(dados[x][0][y].get(anos[y])):

                        dados_gerais = dados[x][0][y].get(
                            anos[y])[z].get(tipos[s])

                        if anos[y] == anos[0]:
                            dados_primeiro_ano.append(dados_gerais)
                        if anos[y] == anos[1]:
                            dados_segundo_ano.append(dados_gerais)
                        if anos[y] == anos[2]:
                            dados_terceiro_ano.append(dados_gerais)
                        if anos[y] == anos[3]:
                            dados_quarto_ano.append(dados_gerais)
                        if anos[y] == anos[4]:
                            dados_quinto_ano.append(dados_gerais)
                        if anos[y] == anos[5]:
                            dados_sexto_ano.append(dados_gerais)

                        z += 1

                    y += 1

                x += 1
            resultado.append([reduce(soma_lista, dados_primeiro_ano), reduce(soma_lista, dados_segundo_ano), reduce(
                soma_lista, dados_terceiro_ano), reduce(soma_lista, dados_quarto_ano), reduce(soma_lista, dados_quinto_ano), reduce(soma_lista, dados_sexto_ano)])
            s += 1


        w = 0
        dado = {}
        while w < len(anos):

            dado[anos[w]] = {
                'Livros' : resultado[0][w],
                'Artigos' : resultado[1][w],
                'Capitulos' : resultado[2][w]
            }

            w += 1

        df = pd.DataFrame(dado)
        df = df.transpose()

        grafico = Grafico()
        grafico = grafico.grafico_barras(df=df, x=anos, y=['Livros', 'Artigos', 'Capitulos'], height=478, barmode='group', 
                                        color_discrete_map={
                                            "Livros": "#053787",
                                            "Artigos": "#9facc2",
                                            "Capitulos": "#AFAFAF"
                                        },
                                            labels={
                                            'x': '',
                                            'variable': 'Legenda',
                                        }, margin=dict(
                                            l=0, r=30, t=20, b=50), font_color="black", legend=dict(
                                            yanchor="top",
                                            y=0.99,
                                            xanchor="left",
                                            x=0.01
                                        ), bargroupgap=0, bargap=0.3, autosize=True, yaxis_title="",
                                        linecolor='#e0dfda', gridcolor='#e0dfda')
                                        
        titulo = f"Produção da faculdade - ({anos[0]} - {anos[-1]})"

        return grafico, titulo

    def pega_programas(self):
        utils = Utils()
        return utils.pega_programas_departamento().get('programas'), 'Programas'