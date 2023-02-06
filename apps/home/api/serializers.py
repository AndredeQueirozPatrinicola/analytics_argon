from apps.home.models import Docente

from rest_framework import serializers

class GraficoDataSetSerializer(serializers.Serializer):
    label = serializers.CharField()
    backgroundColor = serializers.CharField()
    borderWidth = serializers.IntegerField()
    data = serializers.ListField(child=serializers.IntegerField())

class GraficoDataSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(child=GraficoDataSetSerializer())

class GraficoSerializer(serializers.Serializer):
    type = serializers.CharField()
    data = GraficoDataSerializer()
    responsive = serializers.BooleanField()

class PaginaSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    grafico = GraficoSerializer()
