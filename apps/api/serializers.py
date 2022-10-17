from rest_framework import serializers

from apps.home.models import Docente

class DocenteSerializer(serializers.Serializer):
    
    class Meta:
        model = Docente
        fields = ['docente_id', 'api_docente', 'api_programas', 'api_docentes']
