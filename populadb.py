import requests
import os, django
import pandas as pd
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.utils import Utils
from apps.home.models import Departamento, Docente, Mapa
from services.populadb.Docentes import ApiDocente
from services.populadb.Departamentos import ApiDepartamento


api = 'https://dados.fflch.usp.br/api/'

class PopulaDB():

    def pega_numeros_usp(self):
        response = requests.get('https://dados.fflch.usp.br/api/docentes')
        if response.status_code == 200:
            df = response.json()
            df = pd.DataFrame(df)

            numeros_usp = df['id_lattes'].to_list()
            numeros_usp = [i for i in numeros_usp if i != "0"]

            return numeros_usp
        else:
            print("Algo de errado na requisição")

    def pega_dados_mapas(self):
        """
            Para salvar dados de um novo mapa é necessário colocar o nome dele na lista 'nomes_mapas' além das bases de dados.
            O nome serve como referência nas queries e no banco de dados de forma geral. Certifique-se de não cadastrar
            nomes iguais e de dar um nome adequado. 
        """
        nomes_mapas = ["MapaIndexAlunos",]

        try:
            # Mapa quantidade de alunos(todos) por estado.
            response_base_dados = requests.get(url = 'https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json')
            response_api = requests.get(url = 'https://dados.fflch.usp.br/api/alunosAtivosEstado')

            raw_dados_api = response_api.json()
            raw_base_de_dados = response_base_dados.json()

            for nome in nomes_mapas:

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


if __name__ == '__main__':
    api = PopulaDB()
    utils = Utils()

    try:
        numeros_usp = api.pega_numeros_usp()
        print("Começando a popular tabela de docentes")
        for numero_usp in numeros_usp:
            indice = numeros_usp.index(numero_usp)
            print(f"Docente {numero_usp} | {indice + 1}/{len(numeros_usp)}")

            docente = ApiDocente(numero_usp)
            dados_api_docente = docente.pega_api_docente()
            dados_api_programas = docente.pega_api_programas()
            dados_api_docentes = docente.pega_api_docentes()

            docente.atualiza_ou_cria_docente(dados_api_docente, dados_api_programas, dados_api_docentes)
            sleep(2.5)

        siglas_departamentos = utils.siglas_departamentos('siglas')
        print("Começando a popular tabela de departamentos")
        for sigla in siglas_departamentos:
            print(f"Departamento -> {sigla}:")
            indice = siglas_departamentos.index(sigla)

            departamento = ApiDepartamento(sigla)
            api_docentes = departamento.pega_api_docentes()
            api_programas = departamento.pega_api_programas()
            api_pesquisa_vazio = departamento.pega_api_pesquisa_vazio()
            api_pesquisa_parametros = departamento.pega_api_pesquisa_parametros()
            api_defesas = departamento.pega_api_defesas()
            api_programas_docentes = departamento.pega_api_programas_docentes()
            api_programas_docentes_limpo = departamento.pega_api_programas_docentes_limpo()

            departamento.atualiza_ou_cria_departamento(
                                                    api_docentes,
                                                    api_programas, 
                                                    api_pesquisa_vazio, 
                                                    api_pesquisa_parametros, 
                                                    api_defesas, 
                                                    api_programas_docentes, 
                                                    api_programas_docentes_limpo,  
                                                    )

            sleep(2)

        api.pega_dados_mapas()
        print('Banco de dados populado com sucesso')
    except:
        print("Não foi possivel popular o db, certifique-se que as migrations foram rodadas")
