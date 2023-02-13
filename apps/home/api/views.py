from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response

from apps.home.classes.etl import Etl

from .serializers import GraficoSerializer

import pandas as pd

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

    def plota_grafico(self, tipo, labels, colors, departamento = False):
        titulo = self.get_titulo(departamento)
        data = self.get_data()
        datasets = self.get_datasets(data, colors)
        result = {
            'type' : tipo,
            'data' : {
                'labels' : self.etl.anos,
                'datasets' : datasets
            },
            'options': {
                'plugins' : {
                    'stacked100': { 
                        'enable': True, 
                        'replaceTooltipLabel': False 
                    },
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
            titulo = f"DIstribuição dos alunos de {departamento.capitalize()} por raça(Percentual)."

        return titulo

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico('bar',[
                                                'Amarela', 
                                                'Branca', 
                                                'Indígena', 
                                                'Não informada', 
                                                'Parda',
                                                'Preta'
                                             ],
                                             [
                                                '#052e70',
                                                '#1a448a', 
                                                '#425e8f', 
                                                '#7585a1', 
                                                '#91a8cf',
                                                '#cad5e8'
                                             ], departamento)
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
            titulo = "Distribuição de todos os alunos de graduação por sexo(Percentual)."
        else:
            titulo = f"DIstribuição dos alunos de {departamento.capitalize()} por sexo(Percentual)."

        return titulo

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
        except:
            departamento = False
        finally:
            dados = self.plota_grafico('bar',[
                                               "Mulher",
                                               "Masculino"
                                             ],
                                             [
                                                '#052e70',
                                                '#cad5e8'
                                             ], departamento)
            serializer = GraficoSerializer(dados)
            return Response(serializer.data)
