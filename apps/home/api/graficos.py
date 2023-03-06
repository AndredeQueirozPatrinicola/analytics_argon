from rest_framework import views
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.db.models import Q, Count, Case, When, Sum, IntegerField

from apps.home.classes.etl import Etl
from apps.home.utils import Utils
from apps.home.models import *
from apps.home.classes.departamento import DadosDepartamento, Departamento
from apps.home.classes.departamentos import Departamentos
from apps.home.classes.docente import DadosDocente

from .serializers import GraficoSerializer

import pandas as pd

from datetime import datetime

""" Classes pais que possuem os metodos que não mudam tanto. """
class GraficoAPI(views.APIView):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.etl = Etl()
        self.utils = Utils()

    def get_datasets(self, dados, colors):
        datasets = []
        for dado in dados:
            label = dado[0]
            dado.pop(0)
            data = {
                "label" : label,
                "data" : dado,
                "backgroundColor" : [colors[dados.index(dado)]],
                "borderWidth" : 1
            }
            datasets.append(data)
        return datasets

    def plota_grafico(self, *args, **kwargs):
        titulo = self.get_titulo(kwargs.get('departamento'))
        data = self.get_data()
        labels = self.get_labels()
        datasets = self.get_datasets(data, kwargs['colors'])

        plugins = {
            'title': {
                'display': True,
                'text': titulo,
                'font': {
                    'size' : 16
                }
            }
        }

        if kwargs.get('stacked'):
            plugins['stacked100'] = {
                'enable': True,
                'replaceTooltipLabel': False
            }

        result = {
            'type' : kwargs['tipo'],
            'data' : {
                'labels' : labels,
                'datasets' : datasets
            },
            'options': {
                'plugins' : plugins
            },
            'responsive' : True,
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
                            "label" : "Total",
                            "data" : data,
                            "backgroundColor" : colors,
                            "borderColor" : colors,
                            "borderWidth" : 1
                        }
                    ]
        return datasets

class GraficoDepartamentosDocentesAPIView(GraficoAPI):

    def get_sigla(self):
        sigla = self.utils.siglas_dptos
        if "e" in self.kwargs.get('departamento').split():
            departamento = self.kwargs.get('departamento').split()
            departamento_formatado = []
            for palavra in departamento:
                if palavra != "e":
                    palavra = palavra.capitalize()
                departamento_formatado.append(palavra)
            departamento_formatado = " ".join(departamento_formatado)
            sigla = sigla.get(departamento_formatado)
        else:
            sigla = sigla.get(self.kwargs.get('departamento').title())
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

    def get_data(self):
        if graduacao:=self.kwargs.get('graduacao'):
            resultado = self.etl.pega_dados_por_ano('raca', order_by='raca', where=graduacao)
        else:
            resultado = self.etl.pega_dados_por_ano('raca', order_by='raca')
            
        dados = pd.DataFrame(resultado)
        dados = dados.fillna(0)
        dados = dados.values.tolist()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição de todos os alunos de graduação por raça/ano(Percentual)."
        else:
            return f"DIstribuição dos alunos de {departamento.title()} por raça/ano(Percentual)."
        
    def get_labels(self):
        return [int(ano) for ano in range(int(datetime.now().year)- 6, int(datetime.now().year + 1))]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'bar', colors = [
                                                          '#cad5e8',  '#1a448a',  '#425e8f', 
                                                          '#7585a1', '#91a8cf', '#052e70', 
                                                      ], 
                                            stacked = True, departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)


class GraficoSexoAPIView(GraficoAPI):

    def get_data(self):
        if graduacao:=self.kwargs.get('graduacao'):
            dados = self.etl.pega_dados_por_ano("sexo", order_by='sexo', where=graduacao)
        else:
            dados = self.etl.pega_dados_por_ano("sexo", order_by='sexo')
        dados = pd.DataFrame(dados)
        dados = dados.values.tolist()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Distribuição de todos os alunos de graduação por sexo/ano(Percentual)."
        else:
            return f"Distribuição dos alunos de {departamento.title()} por sexo/ano(Percentual)."

    def get_labels(self):
        return [int(ano) for ano in range(int(datetime.now().year)- 6, int(datetime.now().year + 1))]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'bar',colors = [
                                                                '#91a8cf', 
                                                                '#052e70'
                                                             ], 
                                       stacked = True, departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        

class GraficoPizzaSexo(GraficoPizzaAPIView):

    def get_data(self):
        if graduacao:=self.kwargs.get('graduacao'):
            dados = AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacao='ativo', alunos_graduacao__nomeCurso=graduacao).values('sexo').annotate(count=Count('*'))
        else:
            dados = AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacao='ativo').values('sexo').annotate(count=Count('*'))
        
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
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'pie',colors = [
                                                                '#91a8cf',
                                                                '#052e70'  
                                                             ], 
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoPizzaRaca(GraficoPizzaAPIView):

    def get_data(self):
        if graduacao:=self.kwargs.get('graduacao'):
            dados = AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacao='ativo', alunos_graduacao__nomeCurso=graduacao).values('raca').annotate(count=Count('*')).order_by('raca')
        else:
            dados = AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacao='ativo').values('raca').annotate(count=Count('*')).order_by('raca')
        
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
            return f"Distribuição dos alunos de {departamento.title()} por sexo(Percentual)."

    def get_labels(self):
        return ["Amarela", "Branca", "Indígena", "Não informada", "Parda", "Preta"]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'pie', colors = [
                                                          '#cad5e8',  '#1a448a',  '#425e8f', 
                                                          '#7585a1', '#91a8cf', '#052e70', 
                                                      ],  
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        

class GraficoProducaoHistoricaDepartamentos(GraficoDepartamentosDocentesAPIView):

    def get_data(self):
        if self.kwargs.get('departamento'):
            query = self.queries(departamento = ['api_programas_docente'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_prod_serie_historica(query)
        else:
            query_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente')
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
        return [int(ano) for ano in range(int(datetime.now().year)- 6, int(datetime.now().year))]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['departamento']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'bar', colors = [
                                                        '#052e70', '#7585a1', 
                                                        '#91a8cf',
                                                      ],  
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoProducaoDepartamentos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    def get_data(self):
        if self.kwargs.get('departamento'):
            query = self.queries(departamento = ['api_programas_docente_limpo'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_prod_departamento(query)
        else:
            query_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente')
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
            departamento = self.kwargs['departamento']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'pie', colors = [
                                                        '#052e70', '#7585a1', 
                                                        '#91a8cf',
                                                      ],  
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoBolsaSemICePosDoc(GraficoDepartamentosDocentesAPIView):

    def get_data(self):
        if self.kwargs.get('departamento'):
            query = self.queries(departamento = ['api_pesquisa_parametros'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_grafico_bolsa_sem(query)
        else:
            query_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.grafico_bolsa_sem()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Projetos de Iniciação Ciêntifica e pós-doutorado com e sem bolsa de todos os departamentos"
        else:
            return f"Projetos de Iniciação Ciêntifica e pós-doutorado com e sem bolsa de {departamento.title()}"
    
    def get_labels(self):
        return [int(ano) for ano in range(int(datetime.now().year)- 6, int(datetime.now().year))]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['departamento']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico( tipo = 'bar',colors = [
                                                        '#052e70', '#1a448a', 
                                                        '#425e8f', '#7585a1', 
                                                        '#91a8cf', '#cad5e8'
                                                      ], 
                                        departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoDefesasDepartamentos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    def get_data(self):
        if self.kwargs.get('departamento'):
            query = self.queries(departamento = ['api_defesas'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.defesas_mestrado_doutorado(query)
        else:
            query_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.grafico_defesas()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Proporção entre alunos de Mestrado, Doutorado e Doutorado Direto de toda a faculdade."
        else:
            return f"Proporção entre alunos de Mestrado, Doutorado e Doutorado Direto no departamento de {departamento.title()}."

    def get_labels(self):
        return ["Mestrado", "Doutorado", "Doutorado Direto"]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['departamento']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'pie', colors = [
                                                        '#052e70', '#7585a1', 
                                                        '#91a8cf',
                                                      ],  
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoDocentesNosDepartamentos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    def get_data(self):
        query_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
        query_docentes = Docente.objects.values('api_docentes')
        departamentos = Departamentos(query_departamentos, query_docentes)
        departamentos.plota_tipo_vinculo_docente()
        dados = departamentos.plota_relacao_cursos()
        return dados

    def get_titulo(self, departamento):
        return "Distribuição dos docentes pelos departamentos da faculdade."

    def get_labels(self):
        return ['Letras Clássicas e Vernáculas', 'Letras Modernas', 'História', 'Geografia', 'Filosofia', 'Letras Orientais', 'Sociologia', 'Lingüística', 'Antropologia', 'Ciência Política', 'Teoria Literária e Literatura Comparada']

    def get(self, *args, **kwargs):
        dados = self.plota_grafico(tipo = 'pie', colors = [
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
                                                    ],  
                                    departamento = False)
        serializer = GraficoSerializer(dados)
        return Response(serializer.data)
    
class GraficoTipoVinculo(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    def get_data(self):
        if self.kwargs.get('departamento'):
            query = self.queries(docente = ['api_docentes'])
            departamento = DadosDepartamento(self.get_sigla())
            dados = departamento.plota_tipo_vinculo_docente(query)
        else:
            query_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
            query_docentes = Docente.objects.values('api_docentes')
            departamentos = Departamentos(query_departamentos, query_docentes)
            dados = departamentos.plota_tipo_vinculo_docente()
        return dados

    def get_titulo(self, departamento):
        if not departamento:
            return "Proporção entre tipos de vínculo dos docentes de toda a universidade"
        else:
            return f"Proporção entre tipos de vínculo dos docentes do departamento de {departamento.title()}."

    def get_labels(self):
        return ['Prof Doutor', 'Prof Associado', 'Prof Titular', 'Prof Contratado III', 'Assistente', 'Prof Colab Ms-6', 'Prof Contratado II']

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['departamento']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'pie', colors = [
                                                    '#2d528d',
                                                    '#486492',
                                                    '#6980a7',
                                                    '#8291ac',
                                                    '#9faec9',
                                                    '#969ca8',
                                                    '#c5cad3',
                                                    ],
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoOrientandos(GraficoDepartamentosDocentesAPIView, GraficoPizzaAPIView):

    def get_data(self):
        docente = DadosDocente(self.kwargs.get('docente'))
        query = Docente.objects.filter(docente_id=self.kwargs.get('docente')).values('api_docente')
        query = query[0]
        return docente.plota_grafico_orientandos(query.get('api_docente'))

    def get_titulo(self, departamento):
        return f"Proporção entre os níveis de pós-graduação dos orientandos."

    def get_labels(self):
        return ['Mestrado', "Doutorado", "Doutorado Direto"]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['docente']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico(tipo = 'pie', colors = [
                                                    '#2d528d',
                                                    '#486492',
                                                    '#6980a7',
                                                    '#8291ac',
                                                    '#9faec9',
                                                    '#969ca8',
                                                    '#c5cad3',
                                                    ],
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoProducaoHistoricaDocente(GraficoPizzaAPIView):

    def get_data(self):
        docente = DadosDocente(self.kwargs.get('docente'))
        query = Docente.objects.filter(docente_id=self.kwargs.get('docente')).values('api_docente')
        query = query[0]
        if tipo:=self.kwargs.get('tipo'):
            return docente.plota_grafico_historico(tipo , query.get('api_docente'))
        else:
            return docente.plota_grafico_historico('artigos', query.get('api_docente'))

    def get_titulo(self, departamento):
        if tipo:=self.kwargs.get('tipo'):
            return f"Produção histórica de {self.kwargs.get('tipo').capitalize()} do docente."
        else:
            return f"Produção histórica de livros do docente."

    def get_labels(self):
        data = self.get_data()
        ano_ini = data[0][0]
        return [int(ano) for ano in range(int(ano_ini), int(datetime.now().year) + 1)]   

    def get(self, *args, **kwargs):
        try:
            docente = self.kwargs['docente']
            dados = self.plota_grafico(tipo = 'line', colors = [
                                                    '#97bde8'
                                                    ],
                                        departamento = docente)

            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        except:
            return Response({'error' : 406})