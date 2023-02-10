from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer 

from apps.home.classes.graduacao import Graduacao

from .serializers import GraficoSerializer

class GraduacaoRacaAPIView(views.APIView):

    def get(self, *args, **kwargs):
        try:
            departamento = self.kwargs['graduacao']
            graduacao = Graduacao(departamento)
        except:
            departamento = False
            graduacao = Graduacao()

        dados = graduacao.trata_dados_raca_api('bar',[
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
