from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer 

from apps.home.classes.graduacao import Graduacao

from .serializers import GraficoRacaAnoSerializer

class Grafico():

    def __init__(self, array_x, array_y, titulo:str):
        self.array_x = array_x
        self.array_y = array_y
        self.titulo = titulo



class GraduacaoAPIView(views.APIView):

    def get(self, request):
        graduacao = Graduacao()
        dados = graduacao.pega_dados_raca()
        serializer = GraficoRacaAnoSerializer(dados, many=True)
        return Response(serializer.data)


