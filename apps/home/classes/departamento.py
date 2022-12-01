import pandas as pd
from datetime import datetime
import requests


from apps.home.models import Departamento, Docente
from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils

class DadosDepartamento():

    def __init__(self, sigla):
        self.sigla = sigla

    def tabela_docentes(self, api_programas, api_docentes):
        dados_programas = api_programas
        dados_docentes = api_docentes

        for i in dados_programas:
            if i['sigla'] == self.sigla:
                nome = i['nome']
                id = i['id_lattes_docentes']
                codset = i['codigo']

        docentes = [i for i in dados_docentes if int(i['codset']) == int(codset)]

        df = pd.DataFrame(docentes)

        id_lattes = df['id_lattes']
        resultado = {
            'df' : df,
            'id_lattes' : id_lattes,
            'nome' : nome,
            'id' : id
        }

        return resultado

    def pega_numero_docentes(self, api_programas, api_docentes):
        departamento = api_programas
        resultado = api_docentes

        total = 0
        ativos = 0
        aposentados = 0

        for i in resultado:
            if i.get('nomset') == departamento[0].get('nome') or i.get('nomset') == 'Lingüística':
                total += 1
                if i.get('sitatl') == 'A':
                    
                    ativos += 1
                elif i.get('sitatl') == 'P':
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

    def plota_aposentados_ativos(self, api_programas, api_docentes):
        numero_docentes = self.pega_numero_docentes(api_programas, api_docentes)
        ativos_aposentados = [numero_docentes.get('numeros').get('ativos'), numero_docentes.get('numeros').get('aposentados')]
        tipos = ['Ativos', "Aposentados"]
        titulo = 'Percentual entre docentes aposentados e ativos'
        grafico = Grafico()
        grafico = grafico.grafico_pizza(values=ativos_aposentados, names=tipos,
                                        color=tipos, color_discrete_sequence=["#052e70", "#AFAFAF"], margin={'l': 20, 'r': 20, 't': 20, 'b': 20})

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def plota_tipo_vinculo_docente(self, api_docentes):
        dados = api_docentes

        x = 0
        nomefnc = []
        while x < len(dados):
            nomefnc.append(dados[x].get('nomefnc'))

            x += 1

        df = pd.DataFrame(nomefnc)

        lista_nomes = df.value_counts().index.to_list()
        nomes = [i[0] for i in lista_nomes]
        lista_valores = df.value_counts().to_list()

        titulo = 'Percentual entre tipos de vínculo de docente'
        grafico = Grafico()
        grafico = grafico.grafico_pizza(values=lista_valores, names=nomes, color=nomes, legend_orientation='h',
                                        color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"], x=1, y=1.02,
                                        margin={'l': 20, 'r': 20, 't': 20, 'b': 20})

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def plota_prod_departamento(self, api_programas_docente_limpo):
        dados = api_programas_docente_limpo
        df = pd.DataFrame(dados)
        somas = df['total_livros'].to_list(), df['total_artigos'].to_list(), df['total_capitulos'].to_list()

        x = 0
        lista_valores = []
        while x < len(somas):
            lista_valores_individuais = [int(i) for i in somas[x]]
            lista_valores.append(sum(lista_valores_individuais))
            x += 1


        grafico = Grafico()
        grafico = grafico.grafico_barras(x=['Livros', 'Artigos', 'Capitulos'], y=lista_valores, color=['Livros', 'Artigos', 'Capitulos'],
                     color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"],
                     linecolor='#e0dfda', gridcolor='#e0dfda', margin=dict(
                     l=15, r=15, t=15, b=0), legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01),
                     labels={
                        'x': '',
                        'color' : 'Legenda'
                     })

        titulo = 'Produção total do departamento registrada no Lattes'

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def tabela_trabalhos(self, api_pesquisa):
        dados = api_pesquisa

        df = pd.DataFrame(dados)
        df = pd.DataFrame(df[self.sigla])
        df = df.rename(index={
            'nome_departamento': "Nome do departamento",
            'ic_com_bolsa': "IC com bolsa",
            'ic_sem_bolsa': "IC sem bolsa",
            'pesquisadores_colab': 'Pesquisadores colaboradores ativos',
            'projetos_pesquisa': 'Projetos de pesquisa dos Docentes',
            'pesquisas_pos_doutorado_com_bolsa': 'Pesquisas pós doutorado com bolsa',
            'pesquisas_pos_doutorado_sem_bolsa': 'Pesquisas pós doutorado sem bolsa'
        })
        indices = df.index
        indices.to_list()
        valores = df[self.sigla].to_list()

        x = 0
        dados_tabela = []
        while x < len(indices):
            tabela_dados = [indices[x], valores[x]]
            dados_tabela.append(tabela_dados)
            x += 1

        headers = ['Nomes', 'Valores']

        resultado = {
            'headers' : headers,
            'tabelas' : dados_tabela
        }

        return resultado

    def plota_grafico_bolsa_sem(self, api_pesquisa_parametros):
        dados = api_pesquisa_parametros

        anos = [i for i in range(int(datetime.now().year) - 6, datetime.now().year)]
        anos_str = [str(i) for i in anos]

        df = pd.DataFrame(dados[0])
        df = df.drop(['pesquisadores_colab'])
        df = df.transpose()
        df = df.rename(columns={
            "ic_com_bolsa": "IC com bolsa",
            "ic_sem_bolsa": "IC sem bolsa",
            'pesquisas_pos_doutorado_com_bolsa': 'Pesquisas pós doutorado com bolsa',
            'pesquisas_pos_doutorado_sem_bolsa': 'Pesquisas pós doutorado sem bolsa'
        })

        grafico = Grafico()
        grafico = grafico.grafico_barras(df=df, x=anos_str, y=['IC com bolsa', 'IC sem bolsa', 'Pesquisas pós doutorado com bolsa', 'Pesquisas pós doutorado sem bolsa'],
                           barmode='group', height=400, color_discrete_map={
            "IC com bolsa": "#053787",
            "IC sem bolsa": "#264a87",
            "Pesquisas pós doutorado com bolsa": "#9facc2",
            "Pesquisas pós doutorado sem bolsa": "#AFAFAF"},
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

        titulo = f"Relação entre IC's e Pesquisas de pós com e sem bolsa - ({anos[0]} - {anos[-1]})"

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def plota_prod_serie_historica(self, api_programas_docente):
        dados = api_programas_docente

        anos_int = [i for i in range(int(datetime.now().year) - 6, datetime.now().year)]
        anos = [str(i) for i in anos_int]

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
        f = len(dados[0].get(anos[0]))

        while f < len(lista_livros) + len(dados[0].get(anos[0])):

            resultado_livros.append(sum(lista_livros[g:f]))
            resultado_artigos.append(sum(lista_artigos[g:f]))
            resultado_capitulos.append(sum(lista_capitulos[g:f]))

            g = f
            f += len(dados[0].get(anos[0]))

        resultado = {}
        s = 0
        while s < len(anos_int):

            resultado[anos_int[s]] = {
                'total_livros': resultado_livros[s],
                'total_artigos': resultado_artigos[s],
                'total_capitulos': resultado_capitulos[s]
            }

            s += 1

        df = pd.DataFrame(resultado)
        df = df.transpose()
        df = df.rename(columns={'total_livros': 'Livros',
                       'total_artigos': 'Artigos', 'total_capitulos': 'Capitulos'})
        
        grafico = Grafico()
        grafico = grafico.grafico_barras(df=df, x=anos, y=['Livros', 'Artigos', 'Capitulos'], height=478, barmode='group', color_discrete_map={
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
        
        titulo = f"Produção do departamento - ({anos[0]} - {anos[-1]})"

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico 
        }

        return resultado

    def pega_programa_departamento(self):
        programas_dpto = Utils()
        programas_dpto = programas_dpto.pega_programas_departamento(self.sigla)
        programas_dpto = programas_dpto.get('programas')

        label = 'Programas'

        resultado = {
            'label' : label,
            'programas_dpto' : programas_dpto
        }

        return resultado
    
    def grafico_defesas(self, api_defesas):
        meses = [mes for mes in range(1, 13)]
        dados = {key : value*0 for (key, value) in zip(meses, meses) }
        ano_atual = datetime.now().year - 1

        for defesa in api_defesas:
            
            data = defesa.get('data')
            verifica_mes = int(data.split('/')[1])
            dados[verifica_mes] = dados.get(verifica_mes) + 1

        
        df = pd.DataFrame(dados, index = [0])
        df = df.transpose()
        df = df.rename(columns = {0:'Numero defesas'})

        grafico = Grafico()
        grafico = grafico.grafico_linhas(df=df, x=df.index, y='Numero defesas', height=450, tickmode='linear',labels={
                'index': 'Mês',
            }, margin=dict(l=0, r=30, t=20, b=50), font_color="black", showlegend=False, linecolor='#e0dfda', gridcolor='#e0dfda')

        resultado = {
            'titulo' : f'Defesas realizadas no ano de {ano_atual}',
            'grafico' : grafico,
        }

        return resultado
        

    
    def pega_tabela_defesas(self, api_defesas):
        utils = Utils()          

        resultado = []
        for defesa in api_defesas:
            
            codigo_departamento = defesa.get('codare')
            verifica_departamento = utils.pega_departamento_programa(codigo_departamento)

            if verifica_departamento.get('sigla') == self.sigla:
                    resultado.append(
                    [
                        defesa.get('titulo'),
                        defesa.get('nome'),
                        defesa.get('nivel'),
                        defesa.get('nomare'),
                        defesa.get('data'),
                    ]
                )

        resultado = {
            'titulo' : f'Defesas realizadas no ano de {datetime.now().year-1}',
            'headers' : ['Titulo', 'Nome', 'Nivel', 'Programa', 'Data'],
            'tabela' : resultado
        }

        return resultado

    def defesas_mestrado_doutorado(self, api_defesas):
        tipos = ['ME', 'DO', 'DD']

        x, y, z = 0, 0, 0
        nivel = []
        for defesa in api_defesas:  

            if defesa.get('nivel') == 'ME':
                x += 1
            if defesa.get('nivel') == 'DO':
                y += 1
            if defesa.get('nivel') == 'DD':
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