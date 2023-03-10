import requests
from django.test import TestCase, Client, RequestFactory

from apps.home import models

class IndexViewTestCase(TestCase):

    def setUp(self) -> None:
        self.base_de_dados = requests.get(url = 'https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json').json()
        self.dados_do_mapa = requests.get(url = 'https://dados.fflch.usp.br/api/alunosAtivosEstado').json()
        self.mapa = models.Mapa.objects.create(
            nome="MapaAlunosEstados",
            base_de_dados=self.base_de_dados
        )


