from apps.home.models import Docente

from rest_framework import serializers


class OptionsSerializer(serializers.Serializer):
    plugins = serializers.DictField(child=serializers.DictField())
    legend = serializers.DictField(child = serializers.DictField(), required=False)

class GraficoDataSetSerializer(serializers.Serializer):
    label = serializers.CharField()
    backgroundColor = serializers.ListField(child=serializers.CharField())
    borderColor = serializers.ListField(child=serializers.CharField(), required=False)
    borderWidth = serializers.IntegerField()
    data = serializers.ListField(child=serializers.IntegerField())

class GraficoDataSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(child=GraficoDataSetSerializer())

class GraficoSerializer(serializers.Serializer):
    type = serializers.CharField()
    data = GraficoDataSerializer()
    options = OptionsSerializer()
    responsive = serializers.BooleanField()
