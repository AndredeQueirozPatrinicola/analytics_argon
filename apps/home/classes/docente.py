import pandas as pd
import requests
from datetime import datetime


from apps.home.models import Docente
from apps.home.classes.graficos import Grafico


API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'


class DadosDocente():

    def __init__(self, parametro, sigla):
        self.parametro = parametro
        self.sigla = sigla

    def pega_vinculo_situacao(self):
        """
            Pega dados no BD equivalentes à: https://dados.fflch.usp.br/api/docentes

            Trata dados e retorna o vinculo e a situacao do docente. 
        """
        dados = Docente.objects.filter(docente_id = self.parametro).values_list('api_docentes')

        dados = dados[0][0]

        vinculo = dados.get('nomefnc')
        situacao = dados.get('sitatl')
        
        if situacao == 'A':
            situacao = "Ativo"
        elif situacao == 'P':
            situacao = "Aposentado"
        else:
            return "Não informado"

        return vinculo, situacao

    def linhas_de_pesquisa(self):
        """
            Tenta buscar o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.parametro }}

            e retorna lista com as linhas de pesquisa cadastradas no Lattes.

        """
        api = Docente.objects.filter(docente_id=self.parametro).values_list('api_docente')
        dados = api[0][0]
        linhas_pesquisa = dados.get('linhas_pesquisa')

        linhas_pesquisa = [i.casefold().capitalize() for i in linhas_pesquisa]

        label = 'Linhas'

        return label, linhas_pesquisa

    def pega_caminho(self):
        """
            Tenta obter os dados necessários do banco de dados e caso não
            consiga visita a api para pega-los. 
            
            Docentes aposentados necessitam da visita na API.

            Retorna lista de dicionários com caminho
        """
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
                'url': "/departamentos/" + self.sigla
            },
            {
                'text': dados_nome.get('nome'),
                'url': '#'
            }
        ]

        return caminho

    def plota_grafico_historico(self, tipo):
        """
            Recebe o parametro tipo -> "livro", "capitulo", "artigo" e
            retorna gráfico de linhas com toda produção por ano do docente.
        """
        try:
            api = Docente.objects.filter(docente_id=self.parametro).values_list('api_docente')
            dados = api[0][0]
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

            grafico = Grafico()
            grafico = grafico.grafico_linhas(df=df, x=eixo_x, y=0, height=390, labels={
                'index': '',
                '0': ''
            }, margin=dict(l=0, r=30, t=20, b=50), font_color="white", showlegend=False)

            grafico_titulo = {
                'titulo': f'Produção de {tipo} por ano ({df.index[0]}-{str(datetime.now().year)})',
                'categoria': tipo
            }

            return grafico, grafico_titulo
        except:
            return None, None

    def plota_grafico_pizza(self):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.parametro }}
            e retorna um grafico de pizza com a proporção entre orientandos de Mestrado, Doutorado e Doutorado Direto.
        """
        api = Docente.objects.filter(docente_id=self.parametro).values_list('api_docente')
        dados = api[0][0]

        try:
            df = pd.DataFrame(dados['orientandos'])

            nivpgm = list(df['nivpgm'])
            tipos = ['ME', 'DO', "DD"]

            nivel = []
            x, y, z = 0, 0, 0
            for i in nivpgm:
                if i == 'ME':
                    x += 1
                if i == 'DO':
                    y += 1
                if i == "DD":
                    z += 1

            nivel.append(x)
            nivel.append(y)
            nivel.append(z)

            titulo = [
                {
                    'titulo' : 'Percentual entre mestrandos, doutorandos e doutorandos diretos'
                }
            ]

            figura = Grafico()

            figura = figura.grafico_pizza(values=nivel, names=tipos,  color=tipos, 
                        color_discrete_sequence=["#052e70", "#AFAFAF", "#667691"], 
                        labels={
                            'values': 'Valor',
                            'names': 'Tipo',
                            'color': 'Cor'
                        }, height=490, margin=dict(l=10, r=10, t=10, b=10), legend_orientation="h", y=1.04, x=1)

            return figura, titulo
        except:
            return None, None

    def tabela_orientandos(self):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.parametro }}

            retorna tabela com nome de todos os orientandos de Mestrado, Doutorado e Doutorado Direto
        """
        api = Docente.objects.filter(docente_id=self.parametro).values_list('api_docente')
        dados = api[0][0]
        if dados['orientandos']:
            df = pd.DataFrame(dados['orientandos'])

            nomep = list(df['nompes'])
            nivpgm = list(df['nivpgm'])
            nomare = list(df['nomare'])

            resultado = []
            x = 0
            while x < len(nomep):
                resultado.append([f'{nomep[x]}', f'{nivpgm[x]}', f'{nomare[x]}'])
                x += 1


            tabela_header = [
                {
                    'titulo' : 'Orientandos Ativos',
                    'nome' : 'Nome',
                    'nivel' : 'Nivel',
                    'programa' : 'Programa'
                }
            ]          

            return resultado, tabela_header
        else:
            return None, None

    def tabela_ultimas_publicacoes(self):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.parametro }}

            Retorna lista de listas com dados para tabela com as ultimas 5 publicações de Livros do docente. 
        """
        api = Docente.objects.filter(docente_id=self.parametro).values_list('api_docente')
        dados = api[0][0]

        tabela_publicacoes = [
                {
                    'titulo' : 'Ultimas publicações de livros',
                    'titulo_trabalho' : 'Titulo',
                    'ano' : 'Ano'
                }
            ]

        try:
            tabela = pd.DataFrame(dados['livros'])
            publicacoes = tabela.head(5)
            titulo_ano = publicacoes[['TITULO-DO-LIVRO', 'ANO']]
            publicacao_com_ano = titulo_ano.values.tolist()

            return publicacao_com_ano, tabela_publicacoes

        except:
            return[[ 'Não existem publicações de livros registradas']], tabela_publicacoes
