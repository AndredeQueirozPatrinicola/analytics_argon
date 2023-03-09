import pandas as pd
import requests
from datetime import datetime


from apps.home.models import Docente
from apps.home.classes.graficos import Grafico


API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'
API_DOCENTES = API + 'docentes'


class DadosDocente():

    def __init__(self, numero_lattes, sigla = ""):
        self.numero_lattes = numero_lattes
        self.sigla = sigla


    def pega_informacoes_basicas(self, dados, dados_docente, dados_nome, novo = ""):
        caminho = self.pega_caminho(dados, dados_nome)

        if novo:
            vinculo_situacao = self.pega_vinculo_situacao(dados_nome)
            vinculo = vinculo_situacao.get('vinculo')
            situacao = vinculo_situacao.get('situacao')
            lattes_icon = f"""<a href='http://lattes.cnpq.br/{self.numero_lattes}' target='_blank' >
                                <i class='ai ai-lattes ai-2x f-20 nome-lattes'></i>
                            </a>
                          """
            docente = {
                    "card_header_1" : {
                        "title" : "LATTES",
                        "text" : lattes_icon
                    },
                    "card_header_2" : {
                        "title" : "Linhas de Pesquisa",
                        "text" : self.linhas_de_pesquisa(dados_docente)
                    },
                    "card_header_3" : {
                        'title' : "Tipo de Vinculo",
                        "text" : vinculo
                    },
                     "card_header_4" : {
                        "title" : "Situacao Atual",
                        "text" :  situacao
                    }
                }

        else:
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
        
        linhas_formatadas = []
        for linha in linhas_pesquisa:
            template = f"<span>{linha}</span>"
            linhas_formatadas.append(template)
        linhas_formatadas = " ".join(linhas_formatadas)

        dropdown_linhas = f"""<div class="dropdown" id="dropdown">
                                <div class="dropdown-button card-header-content" id="dropdown-button">
                                    Linhas
                                </div>
                                <div class="dropdown-items">
                                    {linhas_formatadas}
                                </div>
                              </div>
                            """
        return dropdown_linhas

    def pega_caminho(self, dados, dados_nome):
        """
            Tenta obter os dados necessários do banco de dados e caso não
            consiga visita a api para pega-los. 
            
            Docentes aposentados necessitam da visita na API.

            Retorna lista de dicionários com caminho
        """

        try:
            self.nome_departamento = dados[0].get('nome')
        except:
            res = requests.get(url=API_DOCENTES)
            dados = res.json()
            
            for dado in dados:
                if dado.get('id_lattes') == self.numero_lattes:
                    self.nome_departamento = dado.get('nomset')            

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

            resultado = []
            for i in range(int(df.index[0]), int(datetime.now().year) + 1):
                try:
                    resultado.append([str(i), list(df.loc[(str(i))])[0]]) 
                except:
                    resultado.append([str(i), 0])    
            return resultado     
        except:
            return None

    def plota_grafico_orientandos(self, dados):
        """
            Visita o equivalente à: https://dados.fflch.usp.br/api/programas/docente/{{ self.numero_lattes }}
            e retorna um grafico de pizza com a proporção entre orientandos de Mestrado, Doutorado e Doutorado Direto.
        """
        try:
            try:
                dados.get('api_docentes')
            except:
                pass

            df = pd.DataFrame(dados['orientandos'])
            nivpgm = list(df['nivpgm'])

            resultado = []
            x, y, z = 0, 0, 0
            for i in nivpgm:
                if i == 'ME':
                    x += 1
                if i == 'DO':
                    y += 1
                if i == "DD":
                    z += 1

            resultado.append(["ME", x])
            resultado.append(["DO", y])
            resultado.append(["DD", z])

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
