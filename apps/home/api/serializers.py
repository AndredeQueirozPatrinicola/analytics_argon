from apps.home.models import Docente

from rest_framework import serializers

class GraficoRacaAnoSerializer(serializers.Serializer):
    ano = serializers.CharField()
    dados = serializers.DictField()

