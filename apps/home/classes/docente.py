import pandas as pd
import requests
from datetime import datetime


from apps.home.models import Docente
from apps.home.classes.graficos import Grafico


API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'


class DadosDocente():

    def __init__(self, numero_lattes, sigla):
        self.numero_lattes = numero_lattes
        self.sigla = sigla


    def pega_informacoes_basicas(self, dados, dados_nome):
        caminho = self.pega_caminho(dados, dados_nome)

        docente = [{
                    'nome': caminho[1].get('text'),
                    'programa': '',
                    'departamento': '',
                    'link_lattes': 'http://lattes.cnpq.br/' + self.numero_lattes
                   }]

        return docente


    def pega_vinculo_situacao(self, dados):
        """
            Pega dados no BD equivalentes à: https://dados.fflch.usp.br/api/docentes

            Trata dados e retorna o vinculo e a situacao do docente. 
        """
        vinculo = dados.get('nomefnc')
        situacao = dados.get('sitatl')
        
        if situacao == 'A':
            situacao = "Ativo"
        elif situacao == 'P':
            situacao = "Aposentado"
        else:
            return "Não informado"

        resultado = {
            'vinculo' : vinculo,
            'situacao' : situacao
        }

        return resultado

    def linhas_de_pesquisa(self, dados):
        """
            Tenta buscar o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.numero_lattes }}

            e retorna lista com as linhas de pesquisa cadastradas no Lattes.

        """
        linhas_pesquisa = dados.get('linhas_pesquisa')
        linhas_pesquisa = [i.casefold().capitalize() for i in linhas_pesquisa]
        label = 'Linhas'

        resultado = {
            'label' : label,
            'linhas_pesquisa' : linhas_pesquisa
        }

        return resultado

    def pega_caminho(self, dados, dados_nome):
        """
            Tenta obter os dados necessários do banco de dados e caso não
            consiga visita a api para pega-los. 
            
            Docentes aposentados necessitam da visita na API.

            Retorna lista de dicionários com caminho
        """
        try:
            self.nome_departamento = dados.get('nome')

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
                'text': dados_nome.get('nompes'),
                'url': '#'
            }
        ]

        return caminho

    def plota_grafico_historico(self, tipo, dados):
        """
            Recebe o numero_lattes tipo -> "livro", "capitulo", "artigo" e
            retorna gráfico de linhas com toda produção por ano do docente.
        """
        try:
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
            }, margin=dict(l=0, r=30, t=20, b=50), font_color="white", showlegend=False, linecolor='#747474', gridcolor='#4d4d4d')

            resultado = {
                'titulo': f'Produção de {tipo} por ano ({df.index[0]}-{str(datetime.now().year)})',
                'categoria': tipo,
                'grafico' : grafico
            }

            return resultado
        except:
            return None

    def plota_grafico_orientandos(self, dados):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.numero_lattes }}
            e retorna um grafico de pizza com a proporção entre orientandos de Mestrado, Doutorado e Doutorado Direto.
        """
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

            figura = Grafico()

            figura = figura.grafico_pizza(values=nivel, names=tipos,  color=tipos, 
                        color_discrete_sequence=["#052e70", "#AFAFAF", "#667691"], 
                        labels={
                            'values': 'Valor',
                            'names': 'Tipo',
                            'color': 'Cor'
                        }, height=490, margin=dict(l=10, r=10, t=10, b=10), legend_orientation="h", y=1.04, x=1)

            resultado = {
                'titulo' : 'Percentual entre mestrandos, doutorandos e doutorandos diretos',
                'grafico' : figura
            }

            return resultado
        except:
            return None


    def tabela_orientandos(self, dados):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.numero_lattes }}

            retorna tabela com nome de todos os orientandos de Mestrado, Doutorado e Doutorado Direto
        """
        try:

            df = pd.DataFrame(dados['orientandos'])
            nomep = list(df['nompes'])
            nivpgm = list(df['nivpgm'])
            nomare = list(df['nomare'])

            resultado = []
            x = 0
            while x < len(nomep):
                resultado.append([f'{nomep[x]}', f'{nivpgm[x]}', f'{nomare[x]}'])
                x += 1

            tabela_infos = {
                    'title' : 'Orientandos Ativos',
                    'nome' : 'Nome',
                    'nivel' : 'Nivel',
                    'programa' : 'Programa'
                }

            tabela = {
                'tabela_infos' : tabela_infos,
                'tabela_conteudo' : resultado
            }          

            return tabela
        except:
            return None

    def tabela_ultimas_publicacoes(self, dados):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.numero_lattes }}

            Retorna lista de listas com dados para tabela com as ultimas 5 publicações de Livros do docente. 
        """
        tabela_publicacoes = {
                    'titulo' : 'Ultimas publicações de livros',
                    'titulo_trabalho' : 'Titulo',
                    'ano' : 'Ano'
                }

        try:
            tabela = pd.DataFrame(dados['livros'])
            publicacoes = tabela.head(5)
            titulo_ano = publicacoes[['TITULO-DO-LIVRO', 'ANO']]
            publicacao_com_ano = titulo_ano.values.tolist()
            resultado = {
                'publicacoes' : publicacao_com_ano,
                'tabela_infos' : tabela_publicacoes
            }

            return resultado

        except:

            resultado = {
                'publicacoes' : [[ 'Não existem publicações de livros registradas']],
                'tabela_infos' : tabela_publicacoes
            }

            return resultado
