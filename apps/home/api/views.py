from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer 

from apps.home.classes.graduacao import Graduacao

from .serializers import GraficoSerializer

class GraduacaoRacaAPIView(views.APIView):

    def get(self, *args, **kwargs):
        try:
            graduacao = Graduacao(self.kwargs['graduacao'])
        except:
            graduacao = Graduacao()

        dados = graduacao.trata_dados_raca_api('bar',[
                                                        'Amarela', 
                                                        'Branca', 
                                                        'Indígena', 
                                                        'Não informada', 
                                                        'Parda'
                                                     ],
                                                     [
                                                        '#052e70',
                                                        '#1a448a', 
                                                        '#425e8f', 
                                                        '#7585a1', 
                                                        '#91a8cf'
                                                     ])
        serializer = GraficoSerializer(dados)
        return Response(serializer.data)
