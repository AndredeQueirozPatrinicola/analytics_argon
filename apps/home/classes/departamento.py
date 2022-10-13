import pandas as pd
from datetime import datetime


from apps.home.models import Departamento, Docente
from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils

class DadosDepartamento():

    def __init__(self, sigla):
        self.sigla = sigla

    def tabela_docentes(self, sigla):
        api_programas = Departamento.objects.filter(
            sigla=sigla).values_list('api_programas')
        api_docentes = Departamento.objects.filter(
            sigla=sigla).values_list('api_docentes')

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
        resultado = Docente.objects.all().values_list('api_docentes')
        departamento = Departamento.objects.filter(sigla=sigla).values_list('api_programas')

        departamento = departamento[0][0][0]

        total = 0
        ativos = 0
        aposentados = 0


        for i in resultado:

            if i[0].get('nomset') == departamento.get('nome') or i[0].get('nomset') == 'Lingüística':
                total += 1
                if i[0].get('sitatl') == 'A':
                    
                    ativos += 1
                elif i[0].get('sitatl') == 'P':
                    aposentados += 1

        resultado = {
            'texto_ativos' : 'Numero de docentes',
            'numero_ativos' : { 
                                'total' : f'Total: {total}',
                                'ativos' : f'Ativos: {ativos}',
                                'aposentados' : f'Aposentados: {aposentados}'
                              }
            }

        return resultado, total, ativos, aposentados

    def plota_aposentados_ativos(self, sigla):
        x, y, ativos, aposentados = self.pega_numero_docentes(sigla)
        ativos_aposentados = [ativos, aposentados]
        tipos = ['Ativos', "Aposentados"]
        titulo = 'Relação entre aposentados e ativos'
        grafico = Grafico()
        grafico = grafico.grafico_pizza(values=ativos_aposentados, names=tipos,
                                        color=tipos, color_discrete_sequence=["#052e70", "#AFAFAF"], margin={'l': 20, 'r': 20, 't': 20, 'b': 20})

        return grafico, titulo

    def plota_tipo_vinculo_docente(self, sigla):
        api = Departamento.objects.filter(
            sigla=sigla).values_list('api_docentes')
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

        titulo = 'Relação entre tipos de vínculo de docente'

        grafico = Grafico()
        
        grafico = grafico.grafico_pizza(values=lista_valores, names=nomes, color=nomes, legend_orientation='h',
                                        color_discrete_sequence=["#052e70", '#264a87', '#667691', '#7d8da8', "#9facc2", "#AFAFAF"], x=1, y=1.02,
                                        margin={'l': 20, 'r': 20, 't': 20, 'b': 20})

        return grafico, titulo

    def plota_prod_departamento(self, sigla):
        api = Departamento.objects.filter(
            sigla=sigla).values_list('api_programas_docente_limpo')
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


        titulo = 'Produção total do departamento'

        return grafico, titulo

    def tabela_trabalhos(self, sigla):
        api = Departamento.objects.filter(
            sigla=sigla).values_list('api_pesquisa')
        dados = api[0][0]

        df = pd.DataFrame(dados)
        df = pd.DataFrame(df[sigla])
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
        valores = df[sigla].to_list()

        x = 0
        dados_tabela = []
        while x < len(indices):
            tabela_dados = [indices[x], valores[x]]
            dados_tabela.append(tabela_dados)
            x += 1

        headers = ['Nomes', 'Valores']

        return dados_tabela, headers

    def plota_grafico_bolsa_sem(self):
        api = Departamento.objects.filter(
            sigla=self.sigla).values_list('api_pesquisa_parametros')
        dados = api[0][0]

        anos = [i for i in range(
            int(datetime.now().year) - 6, datetime.now().year)]
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

        return grafico, titulo

    def plota_prod_serie_historica(self, sigla):
        api = Departamento.objects.filter(
            sigla=sigla).values_list('api_programas_docente')
        dados = api[0][0]

        anos_int = [i for i in range(
            int(datetime.now().year) - 6, datetime.now().year)]
        anos = [str(i) for i in anos_int]

        lista_livros = []
        lista_artigos = []
        lista_capitulos = []
        x = 0
        while x < len(anos):

            z = 0
            while z < len(dados[x].get(anos[x])):
                lista_livros.append(dados[x].get(anos[x])[
                                    z].get('total_livros'))
                lista_artigos.append(dados[x].get(anos[x])[
                                     z].get('total_artigos'))
                lista_capitulos.append(dados[x].get(
                    anos[x])[z].get('total_capitulos'))

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

        return grafico, titulo

    def pega_programa_departamento(self, sigla):
        programas_dpto = Utils.pega_programas_departamento(sigla)
        programas_dpto = programas_dpto.get('programas')

        label = 'Programas'

        return programas_dpto, label