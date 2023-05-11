from rest_framework import views
from rest_framework.response import Response
from django.db.models import Count

from apps.home.classes.etl import Etl
from apps.home.utils import Utils
from apps.home.models import *
from apps.home.classes.departamento import DadosDepartamento, Departamento
from apps.home.classes.departamentos import Departamentos
from apps.home.classes.docente import DadosDocente

from .serializers import GraficoSerializer

import pandas as pd
import re

from datetime import datetime
from functools import cached_property

""" Classes pais que possuem os metodos que não mudam tanto. """


class GraficoAPI(views.APIView):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.etl = Etl()
        self.utils = Utils()
        self.error_message = {
            "error": {"status_code": 400, "message": "Bad Request"}}

    @cached_property
    def get_anos(self):
        ano_inicial = self.request.GET.get("ano_inicial")
        ano_final = self.request.GET.get("ano_final")
        return [int(ano) for ano in range(int(ano_inicial), int(ano_final) + 1)]

    def get_datasets(self, dados, colors):
        datasets = []
        for dado in dados:
            label = dado[0]
            dado.pop(0)
            data = {
                "label": label,
                "data": dado,
                "backgroundColor": [colors[dados.index(dado)]],
                "borderWidth": 1
            }
            datasets.append(data)
        return datasets

    def plota_grafico(self, *args, **kwargs):
        titulo = self.get_titulo(kwargs.get('departamento'))
        data = self.get_data
        labels = self.get_labels()
        datasets = self.get_datasets(data, kwargs['colors'])

        if not data:
            raise(Exception("No-data"))

        plugins = {
            'title': {
                'display': True,
                'text': titulo,
                'font': {
                    'size': 16
                }
            }
        }

        if kwargs.get('stacked'):
            plugins['stacked100'] = {
                'enable': True,
                'replaceTooltipLabel': False
            }

        result = {
            'type': kwargs['tipo'],
            'data': {
                'labels': labels,
                'datasets': datasets
            },
            'options': {
                'plugins': plugins
            },
            'responsive': True,
        }
        return result


class GraficoPizzaAPIView(GraficoAPI):

    def get_datasets(self, dados, colors):
        data = []
        for dado in dados:
            dado.pop(0)
            data.append(*dado)
        datasets = [
            {
                "label": "Total",
                "data": data,
                "backgroundColor": colors,
                "borderWidth": 1
            }
        ]
        return datasets
    
class GraficoLinhasAPIView(GraficoAPI):

    def get_datasets(self, dados, colors):
        
        datasets = []
        for dado in dados:
            label = dado[0]
            dado.pop(0)
            data = {
                "label": label,
                "data": dado,
                "borderColor" : [colors[dados.index(dado)]],
                "backgroundColor": [colors[dados.index(dado)]],
                "borderWidth": 2
            }
            datasets.append(data)
        
        return datasets


class GraficoDepartamentosDocentesAPIView(GraficoAPI):

    def get_sigla(self):
        sigla = self.utils.siglas_dptos
        if "e" in self.request.GET.get('departamento'):
            departamento = self.request.GET.get('departamento').split()
            departamento_formatado = []
            for palavra in departamento:
                if palavra != "e":
                    palavra = palavra.capitalize()
                departamento_formatado.append(palavra)
            departamento_formatado = " ".join(departamento_formatado)
            sigla = sigla.get(departamento_formatado)
        else:
            sigla = sigla.get(self.request.GET.get('departamento').title())
        return sigla

    def queries(self, **kwargs):
        sigla = self.get_sigla()

        if kwargs.get('departamento'):
            query = Departamento.objects.filter(sigla=sigla).values()

            query = query[0]

            resultado_departamentos = {}
            for coluna in kwargs.get('departamento'):
                resultado_departamentos[coluna] = query.get(str(coluna))

            return resultado_departamentos

        if kwargs.get('docente'):
            colunas = kwargs.get('docente')
            query = Docente.objects.values(*colunas)

            resultado = []
            for dado in query:
                resultado.append(dado)

            return resultado


""" Classes filhas que modificam os métodos de acordo com a necessidade de cada grafico """


class GraficoRacaAPIView(GraficoAPI):

    @cached_property
    def get_data(self):
        anos = self.get_anos
        if graduacao := self.request.GET.get('departamento'):
            resultado = self.etl.pega_dados_por_ano(
                            "graduacoes",
                            'raca', coluna_datas=["data_inicio_vinculo", "data_fim_vinculo"], 
                            order_by='raca', where={"nome_curso" : graduacao}, anos=anos)
        else:
            resultado = self.etl.pega_dados_por_ano(
                            "graduacoes",
                            'raca', coluna_datas=["data_inicio_vinculo", "data_fim_vinculo"], 
                            order_by='raca', anos=anos)

        dados = pd.DataFrame(resultado)
        dados = dados.fillna(0)
        dados = dados.values.tolist()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição de todos os alunos de graduação por raça/ano."
        else:
            return f"Distribuição dos alunos de {departamento.title()} por raça/ano."

    def get_labels(self):
        return self.get_anos

    def get(self, *args, **kwargs):
        try:
            if self.request.GET.get('stacked') == 'true':
                stacked = True
            else:
                stacked = False

            departamento = self.request.GET.get('departamento')
            dados = self.plota_grafico(tipo='bar', colors=[
                "#a2c272", "#82C272", "#00A88F", 
                "#0087AC", "#005FAA", "#323B81"
            ], stacked=stacked, departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoSexoAPIView(GraficoAPI):

    @cached_property
    def get_data(self):
        anos = self.get_anos
        if graduacao := self.request.GET.get('departamento'):
            dados = self.etl.pega_dados_por_ano(
                            "graduacoes",
                            "sexo", coluna_datas=["data_inicio_vinculo", "data_fim_vinculo"],order_by='sexo', 
                            where={"nome_curso" : graduacao}, anos=anos)
        else:
            dados = self.etl.pega_dados_por_ano(
                            "graduacoes",
                            "sexo", coluna_datas=["data_inicio_vinculo", "data_fim_vinculo"],
                            order_by='sexo', anos=anos)

        df = pd.DataFrame(dados)
        df[0] = df[0].str.replace("F", "Feminino")
        df[0] = df[0].str.replace("M", "Masculino")
        df = df.values.tolist()
        return df

    def get_titulo(self, departamento):

        if not departamento:
            return "Distribuição de todos os alunos de graduação por sexo/ano."
        else:
            return f"Distribuição dos alunos de {departamento.title()} por sexo/ano."

    def get_labels(self):
        return self.get_anos

    def get(self, *args, **kwargs):
        try:
            if self.request.GET.get('stacked') == 'true':
                stacked = True
            else:
                stacked = False
            departamento = self.request.GET.get('departamento')
            dados = self.plota_grafico(tipo='bar', colors=[
                '#91a8cf',
                '#052e70'
            ], stacked=stacked, departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoRacaSexo(GraficoPizzaAPIView):

    def get_datasets(self, dados, colors):
        datasets = []
        for gender in dados:
            data = []
            for dado in dados.get(gender).get('data'):
                data.append(dado[-1])

            dataset = {
                "label": gender.capitalize(),
                "data": data,
                "backgroundColor": dados.get(gender).get('color'),
                "borderColor": dados.get(gender).get('color'),
                "borderWidth": 1
            }
            datasets.append(dataset)
        return datasets

    @cached_property
    def get_data(self):
        ano = self.request.GET.get('ano')
        if departamento := self.request.GET.get('departamento'):
            raw_data = self.etl.relaciona_dados_em_determinado_ano(column_1='raca', column_2='sexo', table_1='graduacoes', table_2='pessoas', 
                                                               data_inicio=int(ano) - 1, data_fim=ano, departamento=departamento)
        else:
            if not ano: ano = datetime.now().year 
            raw_data = self.etl.relaciona_dados_em_determinado_ano(column_1='raca', column_2='sexo', table_1='graduacoes', table_2='pessoas', 
                                                               data_inicio=int(ano) - 1, data_fim=ano)
        df = pd.DataFrame(raw_data)
        df = df.rename(columns={0: "raca", 1: "sexo", 2: 'count'})
        
        raca_values = df['raca'].unique()
        for raca in raca_values:
            if len(df[df['raca'] == raca]) == 1:
                row = df[df['raca'] == raca]
                gender = row['sexo'].values.tolist()
                if gender[0] == 'F':
                    gender = 'M'
                else:
                    gender = 'F'
                df.loc[len(df)] = [raca, gender, 0]
        
        df = df.sort_values('raca')

        df['sexo'] = df['sexo'].str.replace("F", "Feminino")
        df['sexo'] = df['sexo'].str.replace("M", "Masculino")
        df_male = df.loc[df['sexo'] == 'Masculino']
        df_female = df.loc[df['sexo'] == 'Feminino']

        dados = {
            'Masculino': {
                'data': df_male.values.tolist(),
                'color': "#052e70"
            },
            'Feminino': {
                'data': df_female.values.tolist(),
                'color': "#cad5e8"
            },
        }
        return dados

    def get_titulo(self, departamento):
        ano = self.request.GET.get('ano')
        if departamento:
            return f"Proporção entre Gênero/Raca no departamento de {departamento} em {ano}"
        else:
            if not ano: ano = datetime.now().year
            return f"Proporção entre Gênero/Raca em {ano}"

    def get_labels(self):
        labels = ["Amarela", "Branca", "Indígena",
                  "Não informada", "Parda", "Preta"]
        return labels

    def get(self, *args, **kwargs):
        try:
            if self.request.GET.get('stacked') == 'true':
                stacked = True
            else:
                stacked = False
            departamento = self.request.GET.get('departamento')
            dados = self.plota_grafico(tipo='bar', colors=[
                '#97bde8'
            ], departamento=departamento, stacked=stacked)
            return Response(dados)
        except:
            return Response(self.error_message)


class GraficoPizzaSexo(GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        if graduacao := self.kwargs.get('graduacao'):
            dados = AlunosGraduacao.objects.using('etl').filter(
                alunos_graduacao__situacaoCurso='ativo', alunos_graduacao__nomeCurso=graduacao).values('sexo').annotate(count=Count('*'))
        else:
            dados = AlunosGraduacao.objects.using('etl').filter(
                alunos_graduacao__situacaoCurso='ativo').values('sexo').annotate(count=Count('*'))

        resultado = []
        for dado in dados:
            resultado.append([dado.get('sexo'), dado.get('count')])

        dados = pd.DataFrame(resultado)
        dados = dados.values.tolist()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição de todos os alunos de graduação por sexo(Percentual)."
        else:
            return f"Distribuição dos alunos de {departamento.title()} por sexo(Percentual)."

    def get_labels(self):
        return ["Feminino", "Masculino"]

    def get(self, *args, **kwargs):
        try:
            if departamento := self.kwargs.get('graduacao'):
                departamento = departamento
            else:
                departamento = False
            dados = self.plota_grafico(tipo='pie', colors=[
                '#91a8cf',
                '#052e70'
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoPizzaRaca(GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        if graduacao := self.kwargs.get('graduacao'):
            dados = AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacaoCurso='ativo', alunos_graduacao__nomeCurso=graduacao).values(
                'raca').annotate(count=Count('*')).order_by('raca')
        else:
            dados = AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacaoCurso='ativo').values(
                'raca').annotate(count=Count('*')).order_by('raca')

        resultado = []
        for dado in dados:
            resultado.append([dado.get('raca'), dado.get('count')])

        dados = pd.DataFrame(resultado)
        dados = dados.values.tolist()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição de todos os alunos de graduação por raca(Percentual)."
        else:
            return f"Distribuição dos alunos de {departamento.title()} por raca(Percentual)."

    def get_labels(self):
        return ["Amarela", "Branca", "Indígena", "Não informada", "Parda", "Preta"]

    def get(self, *args, **kwargs):
        try:
            if departamento := self.kwargs.get('graduacao'):
                departamento = departamento
            else:
                departamento = False
            dados = self.plota_grafico(tipo='pie', colors=[
                '#052e70', '#1a448a',  '#425e8f',
                '#7585a1', '#91a8cf', '#cad5e8',
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoProducaoHistoricaDepartamentos(GraficoDepartamentosDocentesAPIView):

    @cached_property
    def get_data(self):
        if self.request.GET.get('departamento') != "Geral" and self.request.GET.get('departamento') != "":
            departamento = self.request.GET.get('departamento')
            query = self.queries(departamento=['api_programas_docente'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_prod_serie_historica(query)
        else:
            query_departamentos = Departamento.objects.values(
                'api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.prod_historica_total()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Produção de Livros, Artigos e Capitulos em todos os departamentos(2017 - 2022)"
        else:
            return f"Produção de Livros, Artigos e Capitulos no departamento de {departamento.title()}(2017-2022)"

    def get_labels(self):
        return [int(ano) for ano in range(int(datetime.now().year) - 6, int(datetime.now().year))]

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            if departamento == 'Geral':
                departamento = False
            
            dados = self.plota_grafico(tipo='bar', colors=[
                '#052e70', '#7585a1',
                '#91a8cf',
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoProducaoDepartamentos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        if self.request.GET.get('departamento') != "Geral" and self.request.GET.get('departamento') != "":
            query = self.queries(departamento=['api_programas_docente_limpo'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_prod_departamento(query)
        else:
            query_departamentos = Departamento.objects.values(
                'api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.prod_total_departamentos()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Produção de Livros, Artigos e Capitulos em todos os departamentos."
        else:
            return f"Produção de Livros, Artigos e Capitulos no departamento de {departamento.title()}."

    def get_labels(self):
        return ["Livros", "Artigos", "Capitulos"]

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            if departamento == 'Geral':
                departamento = False
            
            dados = self.plota_grafico(tipo='pie', colors=[
                '#052e70', '#7585a1',
                '#91a8cf',
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoDefesasDepartamentos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        if self.request.GET.get('departamento') != "Geral" and self.request.GET.get('departamento') != "":
            query = self.queries(departamento=['api_defesas'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.defesas_mestrado_doutorado(query)
        else:
            query_departamentos = Departamento.objects.values(
                'api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.grafico_defesas()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição entre alunos de pós-graduação que realizaram defesas em 2022"
        else:
            return f"Distribuição entre alunos de pós-graduação no departamento de {departamento.title()} que realizaram defesas em 2022."

    def get_labels(self):
        return ["Mestrado", "Doutorado", "Doutorado Direto"]

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            if departamento == 'Geral':
                departamento = False
            
            dados = self.plota_grafico(tipo='pie', colors=[
                '#052e70', '#7585a1',
                '#91a8cf',
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoDocentesNosDepartamentos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        query_departamentos = Departamento.objects.values(
            'api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
        query_docentes = Docente.objects.values('api_docentes')
        departamentos = Departamentos(query_departamentos, query_docentes)
        dados = departamentos.plota_relacao_cursos()
        return dados

    def get_titulo(self, departamento):
        return "Distribuição dos docentes pelos departamentos da faculdade."

    def get_labels(self):
        return ['Letras Clássicas e Vernáculas', 'Letras Modernas', 'História', 'Geografia', 'Filosofia', 'Letras Orientais', 'Sociologia', 'Lingüística', 'Antropologia', 'Ciência Política', 'Teoria Literária e Literatura Comparada']

    def get(self, *args, **kwargs):
        try:
            dados = self.plota_grafico(tipo='pie', colors=[
                '#052e70',
                '#133f85',
                '#2d528d',
                '#486492',
                '#6980a7',
                '#8291ac',
                '#9faec9',
                '#969ca8',
                '#c5cad3',
                '#d6dae0',
                '#f5f6f8',
            ], departamento=False)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoTipoVinculo(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        if self.request.GET.get('departamento') != "Geral" and self.request.GET.get('departamento') != "":
            query = self.queries(docente=['api_docentes'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_tipo_vinculo_docente(query)
        else:
            query_departamentos = Departamento.objects.values(
                'api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.plota_tipo_vinculo_docente()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição dos docentes de acordo com os tipos de vínculo a faculdade"
        else:
            return f"Distribuição dos docentes de acordo com os tipos de vínculo no departamento de {departamento.title()}."

    def get_labels(self):
        return ['Prof Doutor', 'Prof Associado', 'Prof Titular', 'Prof Contratado III', 'Assistente', 'Prof Colab Ms-6', 'Prof Contratado II']

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')
 
            if departamento == 'Geral':
                departamento = False
            
            dados = self.plota_grafico(tipo='pie', colors=[
                '#2d528d',
                '#486492',
                '#6980a7',
                '#8291ac',
                '#9faec9',
                '#969ca8',
                '#c5cad3',
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoOrientandos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        docente = DadosDocente(self.kwargs.get('docente'))
        query = Docente.objects.filter(
            docente_id=self.kwargs.get('docente')).values('api_docente')
        query = query[0]
        return docente.plota_grafico_orientandos(query.get('api_docente'))

    def get_titulo(self, departamento):
        return f"Proporção entre os níveis de pós-graduação dos orientandos."

    def get_labels(self):
        return ['Mestrado', "Doutorado", "Doutorado Direto"]

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            if departamento == 'Geral':
                departamento = False
            
            dados = self.plota_grafico(tipo='pie', colors=[
                '#052e70', '#7585a1',
                '#91a8cf',
            ], departamento=departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoProducaoHistoricaDocente(GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        docente = DadosDocente(self.kwargs.get('docente'))
        query = Docente.objects.filter(
            docente_id=self.kwargs.get('docente')).values('api_docente')
        query = query[0]
        if tipo := self.kwargs.get('tipo'):
            return docente.plota_grafico_historico(tipo, query.get('api_docente'))
        else:
            return docente.plota_grafico_historico('artigos', query.get('api_docente'))

    def get_titulo(self, departamento):
        if tipo := self.kwargs.get('tipo'):
            return f"Produção histórica de {tipo.capitalize()} do docente."
        else:
            return f"Produção histórica de Artigos do docente."

    def get_labels(self):
        data = self.get_data
        ano_ini = data[0][0]
        return [int(ano) for ano in range(int(ano_ini), int(datetime.now().year) + 1)]

    def get(self, *args, **kwargs):
        try:
            docente = self.kwargs['docente']
            dados = self.plota_grafico(tipo='line', colors=[
                '#97bde8'
            ],
                departamento=docente)

            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        
    
class GraficoIngressantesEgressos(GraficoLinhasAPIView):

    @cached_property
    def get_data(self):
        anos = self.get_anos

        if departamento := self.request.GET.get('departamento'):
            dados_inicio_vinculo = self.etl.soma_por_ano("graduacoes", anos, "data_inicio_vinculo", where={"nome_curso" : departamento})
            dados_fim_vinculo = self.etl.soma_por_ano("graduacoes", anos, "data_fim_vinculo", where={"nome_curso" : departamento})
        else:
            dados_inicio_vinculo = self.etl.soma_por_ano("graduacoes", anos, "data_inicio_vinculo")
            dados_fim_vinculo = self.etl.soma_por_ano("graduacoes", anos, "data_fim_vinculo")

        df = pd.DataFrame([], columns=anos)
        df.loc[0] = list(*dados_inicio_vinculo)
        df.loc[1] = list(*dados_fim_vinculo)
        df = df.rename(index={0 : "Ingressantes", 1 : "Egressos"})

        dados = df.values.tolist()
        for dado in dados:
            dado.insert(0, df.index.values.tolist()[dados.index(dado)])
    
        return dados
    
    def get_labels(self):
        return self.get_anos

    def get_titulo(self, departamento):
        if departamento:
            return f"Alunos de graduação ingressantes e egressos do departamento de {departamento}."
        else:
            return "Alunos de graduação ingressantes e egressos."

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            grafico = self.plota_grafico(tipo='line', colors=[
                '#97bde8',
                '#b85149'
            ], departamento=departamento)

            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        

class GraficoTipoIngresso(GraficoLinhasAPIView):

    @cached_property
    def get_data(self):
        labels = ["Fuvest", "Enem", "Transferência Interna e externa"]
        ano_inicial = self.request.GET.get('ano_inicial')
        ano_final = self.request.GET.get('ano_final')
        anos = [int(ano) for ano in range(int(ano_inicial), int(ano_final) + 1)]

        if departamento := self.request.GET.get("departamento"):
            data = self.etl.soma_por_ano("graduacoes", anos, "data_inicio_vinculo", coluna_select="tipo_ingresso", where={"nome_curso" : departamento})
        else:    
            data = self.etl.soma_por_ano("graduacoes", anos, "data_inicio_vinculo", coluna_select="tipo_ingresso")

        df_raw = pd.DataFrame(data)
        fuvest = pd.DataFrame([df_raw[df_raw[0].str.contains(r"FUVEST(?: - Lista extra)?")].sum()], index=[0])
        enem = pd.DataFrame([df_raw[df_raw[0].str.contains(r"SISU|ENEMUSP")].sum()], index=[1])
        transferencia = pd.DataFrame([df_raw[df_raw[0].str.contains(r"Transferência")].sum()], index=[2])
        df = pd.concat([fuvest, enem, transferencia], axis=0)
        
        for i in range(3):
            df.loc[i, 0] = labels[i]

        return df.values.tolist()

    def get_labels(self):
        return self.get_anos

    def get_titulo(self, departamento):
        if departamento:
            return f"Forma de ingresso dos alunos de graduação de {departamento}."
        else:
            return "Forma de ingresso dos alunos de graduação."

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            grafico = self.plota_grafico(tipo='line', colors=[
                '#97bde8',
                '#b85149',
                '#198a11',
            ], departamento=departamento)

            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)


class GraficoTipoEgresso(GraficoAPI):

    @cached_property
    def get_data(self):
        ano_inicial = self.request.GET.get('ano_inicial')
        ano_final = self.request.GET.get('ano_final')
        anos = [int(ano) for ano in range(int(ano_inicial), int(ano_final) + 1)]

        if departamento := self.request.GET.get("departamento"):
            data = self.etl.soma_por_ano("graduacoes", anos, "data_fim_vinculo", coluna_select="tipo_encerramento_bacharel", where={"nome_curso" : departamento})
        else:    
            data = self.etl.soma_por_ano("graduacoes", anos, "data_fim_vinculo", coluna_select="tipo_encerramento_bacharel")

        df_raw = pd.DataFrame(data)

        linhas = []
        for i in range(len(df_raw.index)):
            label = str(df_raw.loc[i, 0])

            if re.search("^Conclusão$", label):
                linhas.append(df_raw.iloc[i].tolist())

            elif re.search("^Cancelamento 0 créditos em dois semestres$", label):
                linhas.append(df_raw.iloc[i].tolist())

            elif re.search("^Desistência", label):
                linhas.append(df_raw.iloc[i].tolist())

            elif re.search("^Abandono 2", label):
                linhas.append(df_raw.iloc[i].tolist())

            elif re.search("^Encerramento", label):
                linhas.append(df_raw.iloc[i].tolist())

            elif re.search("trancamento 4 semestres$", label):
                linhas.append(df_raw.iloc[i].tolist())

        df = pd.DataFrame(linhas)
        return df.values.tolist()

    def get_labels(self):
        return self.get_anos

    def get_titulo(self, departamento):
        if departamento:
            return f"Forma de egresso dos ex-alunos de graduação de {departamento}."
        else:
            return "Forma de egresso dos ex-alunos de graduação."

    def get(self, *args, **kwargs):
        try:
            if self.request.GET.get('stacked') == 'true':
                stacked = True
            else:
                stacked = False
            departamento = self.request.GET.get('departamento')

            grafico = self.plota_grafico(tipo='bar', colors=[
                '#97bde8',
                '#b85149',
                '#fcba03',
                '#198a11',
                '#4f1369',
                "#fc6b03",
                "#03d7fc"
            ], departamento=departamento, stacked=stacked)

            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        

class GraficoTipoBolsa(GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        parameters = {
            "columns" : ["y.nome_fomento", "COUNT(*)"],
            "tables" : ["iniciacoes", "bolsas_ic"],
            "ids" : "id_projeto",
            "condition" : {"situacao_projeto" : "Ativo"},
            "group_by" : ["y.nome_fomento"]
        }

        if departamento := self.request.GET.get("departamento"):
            data = self.etl.group_by(
                                    columns=parameters.get("columns"),
                                    tables=parameters.get("tables"),
                                    ids=parameters.get("ids"),
                                    condition=parameters.get("condition"),
                                    group_by=parameters.get("group_by"),
                                    where = departamento
                                )
        else:
            data = self.etl.group_by(
                                    columns=parameters.get("columns"),
                                    tables=parameters.get("tables"),
                                    ids=parameters.get("ids"),
                                    condition=parameters.get("condition"),
                                    group_by=parameters.get("group_by"),
                                )

        df = pd.DataFrame(data)
        return df.values.tolist()


    def get_labels(self):
        return [i[0] for i in self.get_data]

    def get_titulo(self, departamento):
        if departamento:
            return f"Relação entre tipos de bolsas dos projetos do departamento de {departamento}."
        else:
            return "Relação entre tipos de bolsas dos projetos de todos os departamentos."

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')

            grafico = self.plota_grafico(tipo='pie', colors=[
                "#619ED6", "#6BA547", "#F7D027", "#E48F1B", "#B77EA3", "#E64345", "#60CEED", "#9CF168",
            ], departamento=departamento)

            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        

class GraficoProjetosIcPorAno(GraficoLinhasAPIView):
   
    @cached_property
    def get_data(self):
        anos = self.get_anos

        if departamento := self.request.GET.get("departamento"):
            data = self.etl.soma_por_ano("iniciacoes", anos, "data_inicio_projeto", where={"nome_curso" : departamento})
        else:
            data = self.etl.soma_por_ano("iniciacoes", anos, "data_inicio_projeto")
        
        df = pd.DataFrame(data)
        return df.values.tolist()
    
    def get_titulo(self, departamento):
        if departamento:
            return f"Numero de projetos de IC iniciados por ano no departamento de {departamento}."
        else:
            return "Numero de projetos de IC iniciados por ano."
    
    def get_labels(self):
        return self.get_anos
    
    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')
            grafico = self.plota_grafico(tipo='line', colors=["#97bde8"], departamento=departamento)
            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        

class GraficoIngressantesPosPorNivelPorAno(GraficoLinhasAPIView):

    @cached_property
    def get_data(self):

        map = {"ME" : "Mestrado", "DO" : "Doutorado", "DD" : "Doutorado Direto"}
        
        if departamento := self.request.GET.get('departamento'):
            data = self.etl.soma_por_ano("posgraduacoes", self.get_anos, "primeira_matricula", coluna_select="nivel_programa", where={"nome_area" : departamento})
        else:
            data = self.etl.soma_por_ano("posgraduacoes", self.get_anos, "primeira_matricula", coluna_select="nivel_programa")

        df = pd.DataFrame(data)
        x = 0
        for i in df[0].values:
            df.loc[x, 0] = map.get(i)
            x+=1

        return df.values.tolist()

    def get_titulo(self, departamento):
        
        if departamento:
            return f"Numero de alunos ingressantes no programa de pós-graduacao de {departamento} por ano."
        else:
            return "Numero de alunos ingressantes na pós graduação da FFLCH por ano."

    def get_labels(self):
        return self.get_anos 

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')
            grafico = self.plota_grafico(tipo='line', colors=['#97bde8',
                '#b85149',
                '#198a11',], departamento=departamento)
            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        
class GraficoDistribuicaoNivelPos(GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        
        if departamento := self.request.GET.get('departamento'):
            data = Posgraduacoes.objects.using('etl').values('nivel_programa').filter(nome_area=departamento, tipo_ultima_ocorrencia__in=["ACO", "MAR"]).annotate(total=Count('*'))
        else:
            data = Posgraduacoes.objects.using('etl').values('nivel_programa').filter(tipo_ultima_ocorrencia__in=["ACO", "MAR"]).annotate(total=Count('*'))

        df = pd.DataFrame(data)
        x = 0
        for i in df['nivel_programa'].values:
            df.loc[x, 'nivel_programa'] = self.utils.pos_niveis.get(i)
            x+=1

        return df.values.tolist()

    def get_titulo(self, departamento):
        
        if departamento:
            return f"Numero total de alunos ativos por nível do programa de pós-graduacao de {departamento}."
        else:
            return "Numero total de alunos ativos por nível da pós graduação da FFLCH."

    def get_labels(self):
        return [i[0] for i in self.get_data]

    def get(self, *args, **kwargs):
        try:
            departamento = self.request.GET.get('departamento')
            grafico = self.plota_grafico(tipo='pie', colors=[
                '#b85149',
                '#198a11',
                '#97bde8'], departamento=departamento)
            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        
class GraficoAlunosPorPrograma(GraficoPizzaAPIView):

    @cached_property
    def get_data(self):
        data = Posgraduacoes.objects.using('etl').values('nome_area').filter(tipo_ultima_ocorrencia__in=["ACO", "MAR"]).annotate(total=Count('*')).order_by('total')
        df = pd.DataFrame(data)
        return df.values.tolist()

    def get_titulo(self, departamento):
        return "Numero total de alunos de pós-graduação ativos por programa."

    def get_labels(self):
        return [i[0] for i in self.get_data]

    def get(self, *args, **kwargs):
        try:
            grafico = self.plota_grafico(tipo="bar", colors=['#97bde8'], departamento=False)
            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)
        

class GraficoRacaPorAnoPosGraduacao(GraficoAPI):

    @cached_property
    def get_data(self):
        
        if departamento := self.request.GET.get('departamento'):
            data = self.etl.pega_dados_por_ano("posgraduacoes",
                    "raca", coluna_datas=["primeira_matricula", "data_aprovacao_trabalho"],
                    order_by='raca', anos=self.get_anos, where={"nome_area" : departamento}
                    )
        else:
            data = self.etl.pega_dados_por_ano("posgraduacoes",
                    "raca", coluna_datas=["primeira_matricula", "data_aprovacao_trabalho"],
                    order_by='raca', anos=self.get_anos
                    )

        df = pd.DataFrame(data)
        return df.values.tolist()

    def get_titulo(self, departamento):
        
        if departamento:
            return f"Distribuição dos alunos de pós-graduação de {departamento} por Raça/Ano."
        else:
            return "Distribuição de todos os alunos de pós-graduacao por Raça/Ano."

    def get_labels(self):
        return self.get_anos

    def get(self, *args, **kwargs):
        try:
            if self.request.GET.get('stacked') == 'true':
                stacked = True
            else:
                stacked = False

            departamento = self.request.GET.get('departamento')
            grafico = self.plota_grafico(tipo='bar', colors=[
                "#a2c272", "#82C272", "#00A88F", 
                "#0087AC", "#005FAA", "#323B81"
            ], departamento=departamento, stacked=stacked)
            serializer = GraficoSerializer(grafico)
            return Response(serializer.data)
        except:
            return Response(self.error_message)