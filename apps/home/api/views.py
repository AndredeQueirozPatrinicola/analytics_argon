from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer 

from .serializers import GraficoSerializer

from apps.home.classes.departamentos import Departamentos
from apps.home.models import Docente

class Grafico():

    def __init__(self, array_x, array_y, titulo:str):
        self.array_x = array_x
        self.array_y = array_y
        self.titulo = titulo



@api_view(['GET', 'POST'])
def hello_world(request):
    grafico = Grafico([23,32,12,4], [2,32,12,3], 'titulo')
    serializer = GraficoSerializer(grafico)

    if request.method == 'GET':
        return Response(serializer.data)

