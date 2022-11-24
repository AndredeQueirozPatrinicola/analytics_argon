from rest_framework import serializers

from apps.home.models import Docente

class GraficoSerializer(serializers.Serializer):
    array_x = serializers.ListField(child=serializers.IntegerField())
    array_y = serializers.ListField(child=serializers.IntegerField())
    titulo = serializers.CharField()

    