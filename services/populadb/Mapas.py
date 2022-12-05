import requests
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.utils import Utils
from apps.home.models import Mapa


class ApiMapas:

    def __init__(self) -> None:
        pass


    def pega_dados_mapa_alunos_por_estados(self):
        try:
            # Mapa quantidade de alunos(todos) por estado.
            response_base_dados = requests.get(url = 'https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json')
            response_api = requests.get(url = 'https://dados.fflch.usp.br/api/alunosAtivosEstado')
            nome = 'MapaIndexAlunos'

            raw_dados_api = response_api.json()
            raw_base_de_dados = response_base_dados.json()

            verifica_existencia = Mapa.objects.filter(nome=nome)
            if verifica_existencia.exists():
                # Se por algum motivo a base de dados estiver 
                # vazia o metodo 'verifica_json_vazio'
                # retorna True e não salva no banco de dados.
                protege_base_de_dados = Utils.verifica_json_vazio(raw_base_de_dados)
                if not protege_base_de_dados:
                    Mapa.objects.filter(nome=nome).update(
                                                    base_de_dados=raw_base_de_dados,
                                                    dados_do_mapa=raw_dados_api    
                                                    )
                else:
                    Mapa.objects.filter(nome=nome).update(
                                                    dados_do_mapa=raw_dados_api    
                                                    )
            else:
                salva_dados = Mapa(
                                    nome=nome,
                                    base_de_dados=raw_base_de_dados,
                                    dados_do_mapa=raw_dados_api
                                )
                salva_dados.save()
        except:
            print("Houve um erro para popular o banco de dados de mapa.")
            raise Exception()