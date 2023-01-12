import pandas as pd
import numpy as np
from datetime import datetime
from functools import reduce, cached_property


from apps.home.classes.graficos import Grafico
from apps.home.models import Docente, Departamento
from apps.home.utils import Utils

class Departamentos():

    def __init__(self, api_departamentos, api_docentes):
        self.api_departamentos = api_departamentos
        self.api_docentes = api_docentes

    @cached_property
    def pega_api_docentes(self):
        dados = self.api_docentes
        return [dado.get('api_docentes') for dado in dados]

    @cached_property
    def pega_api_pesquisa_parametros(self):
        dados = self.api_departamentos
        return [dado.get('api_pesquisa_parametros') for dado in dados]

    @cached_property
    def pega_api_programas_docente_limpo(self):
        dados = self.api_departamentos
        return [dado.get('api_programas_docente_limpo') for dado in dados]

    def pega_numero_docentes(self):
        resultado = Docente.objects.count()
        dados = self.pega_api_docentes

        ativos = 0
        aposentados = 0
        total = 0
        for dado in dados:
            total+=1
            if dado.get('sitatl') == 'A':
                ativos += 1
            elif dado.get('sitatl') == 'P':
                aposentados += 1
           
        resultado = {
            'titulo' : 'Numero de docentes',
            'texto_ativos' : { 
                                'total' : f'Total: {total}',
                                'ativos' : f'Ativos: {ativos}',
                                'aposentados' : f'Aposentados: {aposentados}'
                              },
            'numeros' : {
                'total' : total,
                'ativos' : ativos,
                'aposentados' : aposentados
            }}

        return resultado

    def trata_dados_ic(self, dados, anos):
        resultado = {}
        for ano in anos:
            for dado in dados:
                data_per_year = dado.get(ano)
                if dado == dados[0] :
                    ic_com_bolsa = int(data_per_year.get('ic_com_bolsa'))
                    ic_sem_bolsa = int(data_per_year.get('ic_sem_bolsa'))
                    pesquisa_pos_doutorado = int(data_per_year.get('pesquisas_pos_doutorado_com_bolsa'))
                    pesquisa_pos_doutorado_sem_bolsa = int(data_per_year.get('pesquisas_pos_doutorado_sem_bolsa'))
                else:
                    ic_com_bolsa = ic_com_bolsa + int(data_per_year.get('ic_com_bolsa'))
                    ic_sem_bolsa = ic_sem_bolsa + int(data_per_year.get('ic_sem_bolsa'))
                    pesquisa_pos_doutorado = pesquisa_pos_doutorado + int(data_per_year.get('pesquisas_pos_doutorado_com_bolsa'))
                    pesquisa_pos_doutorado_sem_bolsa = pesquisa_pos_doutorado_sem_bolsa + int(data_per_year.get('pesquisas_pos_doutorado_sem_bolsa'))

            resultado_por_ano = {
                    'ic_com_bolsa' : ic_com_bolsa,
                    'ic_sem_bolsa' : ic_sem_bolsa,
                    'pesquisa_pos_doutorado' : pesquisa_pos_doutorado,
                    'pesquisa_pos_doutorado_sem_bolsa' : pesquisa_pos_doutorado_sem_bolsa
                }

            resultado[ano] = resultado_por_ano
        
        return resultado

    def tabela_todos_docentes(self):
        utils = Utils()
        dados = self.pega_api_docentes

        df = pd.DataFrame(dados)
        df = df.drop(columns=['codset'])

        siglas_departamento = []
        for setor in df['nomset']:
            siglas_departamento.append(utils.pega_sigla_por_nome_departamento(setor))

        df['sigset'] = siglas_departamento

        titulo = 'Todos os docentes da faculdade'

        resultado = {
            'titulo' : titulo,
            'df' : df
        }

        return resultado

    def plota_relacao_cursos(self):
        dados = self.pega_api_docentes

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

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def grafico_bolsa_sem(self):
        dados = self.pega_api_pesquisa_parametros
        anos = [str(i) for i in range((datetime.now().year - 6), datetime.now().year)]

        resultado = self.trata_dados_ic(dados, anos)
            
        df = pd.DataFrame(resultado)
        df = df.transpose()
        df = df.rename(columns={'ic_com_bolsa': "IC's com bolsa", 'ic_sem_bolsa': "IC's sem bolsa",
                       'pesquisa_pos_doutorado': "Pos Doutorado com bolsa",'pesquisa_pos_doutorado_sem_bolsa': "Pos Doutorado sem bolsa"})

        fig = Grafico()
        fig = fig.grafico_barras(df=df, x=anos, y=["IC's com bolsa", "IC's sem bolsa", "Pos Doutorado com bolsa", "Pos Doutorado sem bolsa"], barmode='group', height=400, color_discrete_map={
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

        resultado = {
            'titulo' : titulo,
            'grafico' : fig
        }

        return resultado

    def tabela_bolsas(self):
        dados = self.pega_api_pesquisa_parametros
        anos = [str(i) for i in range((datetime.now().year - 6), datetime.now().year)]
        resultado = self.trata_dados_ic(dados, anos)
        rows = ["IC's com bolsa", "IC's sem bolsa", "Pos Doutorado com bolsa", "Pos Doutorado sem bolsa"] 

        df = pd.DataFrame(resultado)
        df = df.rename(columns={
                                'ic_com_bolsa': "IC's com bolsa", 
                                'ic_sem_bolsa': "IC's sem bolsa",
                                'pesquisa_pos_doutorado': "Pos Doutorado com bolsa",
                                'pesquisa_pos_doutorado_sem_bolsa': "Pos Doutorado sem bolsa"})


        lista_valores = df.values.tolist()
        titulos = ['Titulos', ] 
        for ano in anos:
            titulos.append(anos[anos.index(ano)])
        x = 0
        for i in lista_valores:
            i.insert(0, rows[x])
            x += 1

        resultado = {
            'headers' : titulos,
            'tabelas' : lista_valores
        }

        return resultado

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

        resultado = {
            'titulo' : titulo,
            'grafico' : fig
        }

        return resultado

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

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def pega_programas(self):
        utils = Utils()
        resultado = {
            'programas' : utils.pega_programas_departamento().get('programas'),
            'label' : 'Programas'
        }
        return resultado