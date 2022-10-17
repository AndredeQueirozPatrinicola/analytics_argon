from rest_framework import views, viewsets
from rest_framework.response import Response

from .serializers import  DocenteSerializer

from apps.home.classes.departamentos import Departamentos
from apps.home.models import Docente


class DocenteViewSet(viewsets.ViewSet):
    queryset = Docente.objects.all() 
    serializer_class = DocenteSerializer
   