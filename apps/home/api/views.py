from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response

from apps.home.classes.etl import Etl
from apps.home.utils import Utils
from apps.home.models import Docente
from apps.home.classes.departamento import DadosDepartamento, Departamento
from apps.home.classes.departamentos import Departamentos

from .serializers import GraficoSerializer

import pandas as pd

from datetime import datetime

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
        labels = []
        data = []
        for dado in dados:
            dado.pop(0)
            data.append(*dado)
        datasets = [
                        {
                            "label" : "Relação MxF",
                            "data" : data,
                            "backgroundColor" : colors,
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

#########################################
               # Filhos #
#########################################

class GraficoRacaAPIView(GraficoAPI):

    def get_data(self):
        if self.kwargs.get('graduacao'):
            dados = self.etl.pega_dados_por_ano("raca", order_by='raca', where=self.kwargs['graduacao'])
        else:
            dados = self.etl.pega_dados_por_ano("raca", order_by='raca')
        dados = pd.DataFrame(dados)
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
                                                        '#052e70', '#1a448a', 
                                                        '#425e8f', '#7585a1', 
                                                        '#91a8cf', '#cad5e8'
                                                      ], 
                                            stacked = True, departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)


class GraficoSexoAPIView(GraficoAPI):

    def get_data(self):
        if self.kwargs.get('graduacao'):
            dados = self.etl.pega_dados_por_ano("sexo", order_by='sexo', where=self.kwargs['graduacao'])
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
                                                                '#052e70', 
                                                                '#91a8cf', 
                                                             ], 
                                       stacked = True, departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        

class GraficoPizzaSexo(GraficoPizzaAPIView):

    def get_data(self):
        if self.kwargs.get('graduacao'):
            dados = self.etl.query_teste('sexo', self.kwargs['graduacao'])
        else:
            dados = self.etl.query_teste('sexo')

        dados = pd.DataFrame(dados)
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
                                                                '#052e70', 
                                                                '#91a8cf', 
                                                             ], 
                                       departamento = departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
class GraficoPizzaRaca(GraficoPizzaAPIView):

    def get_data(self):
        if self.kwargs.get('graduacao'):
            dados = self.etl.query_teste('raca', self.kwargs['graduacao'])
        else:
            dados = self.etl.query_teste('raca')

        dados = pd.DataFrame(dados)
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
                                                        '#052e70', '#1a448a', 
                                                        '#425e8f', '#7585a1', 
                                                        '#91a8cf', '#cad5e8'
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