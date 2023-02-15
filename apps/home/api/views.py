from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response

from apps.home.classes.etl import Etl

from .serializers import GraficoSerializer

import pandas as pd

from datetime import datetime

class GraficoAPI(views.APIView):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.etl = Etl()

    def get_datasets(self, dados, colors):
        datasets = []
        for dado in dados:
            label = dado[0]
            dado.pop(0)
            data = {
                "label" : label,
                "data" : dado,
                "backgroundColor" : colors[dados.index(dado)],
                "borderWidth" : 1
            }
            datasets.append(data)
        return datasets

    def plota_grafico(self, *args, **kwargs):
        titulo = self.get_titulo(kwargs.get('departamento'))
        data = self.get_data()
        labels = self.get_labels()
        datasets = self.get_datasets(data, kwargs['colors'])

        result = {
            'type' : kwargs['tipo'],
            'data' : {
                'labels' : labels,
                'datasets' : datasets
            },
            'options': {
                'plugins' : {
                    'title': {
                        'display': True,
                        'text': titulo,
                        'font': {
                            'size' : 16
                        }
                    }
                }
            },
            'responsive' : True,
        }
        if kwargs.get('stacked'):
            result.get('options')['plugins'] = {'stacked100': { 
                        'enable': True, 
                        'replaceTooltipLabel': False 
                    },}

        return result

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
            titulo = "Distribuição de todos os alunos de graduação por raça(Percentual)."
        else:
            return f"DIstribuição dos alunos de {departamento.capitalize()} por raça(Percentual)."
        
    def get_labels(self):
        return [int(ano) for ano in range(datetime.now()- 6, datetime.now() + 1)]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico('bar',colors = [
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
            return "Distribuição de todos os alunos de graduação por sexo(Percentual)."
        else:
            return f"Distribuição dos alunos de {departamento.capitalize()} por sexo(Percentual)."

    def get_labels(self):
        return [int(ano) for ano in range(datetime.now()- 6, datetime.now() + 1)]

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico('bar',colors = [
                                                        '#052e70', '#1a448a', 
                                                        '#425e8f', '#7585a1', 
                                                        '#91a8cf', '#cad5e8'
                                                      ], 
                                            stacked = True, departamento = departamento)
            
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
        
