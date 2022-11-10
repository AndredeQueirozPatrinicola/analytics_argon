import requests
import os, django
import pandas as pd
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.utils import Utils
from services.populadb.Docentes import ApiDocente
from services.populadb.Departamentos import ApiDepartamento
from services.populadb.Mapas import ApiMapas


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

    def popula_docente(self):
        numeros_usp = self.pega_numeros_usp()
        print("Começando a popular tabela de docentes...")
        for numero_usp in numeros_usp:
            indice = numeros_usp.index(numero_usp)
            print(f"Docente {numero_usp} | {indice + 1}/{len(numeros_usp)}")

            docente = ApiDocente(numero_usp)
            dados_api_docente = docente.pega_api_docente()
            dados_api_programas = docente.pega_api_programas()
            dados_api_docentes = docente.pega_api_docentes()

            docente.atualiza_ou_cria_docente(dados_api_docente, dados_api_programas, dados_api_docentes)
            sleep(3)

    def popula_departamentos(self):
        siglas_departamentos = utils.siglas_departamentos('siglas')
        print("Começando a popular tabela de departamentos...")
        for sigla in siglas_departamentos:
            print(f"Departamento -> {sigla}:")

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

            sleep(3)

    def popula_mapas(self):
        print("Começando a popular tabela de mapas...")
        mapa = ApiMapas()
        mapa.pega_dados_mapa_alunos_por_estados()


if __name__ == '__main__':
    api = PopulaDB()
    utils = Utils()

    try:
        api.popula_docente()
        api.popula_departamentos()
        api.popula_mapas()
        print('Banco de dados populado com sucesso')
    except:
        print("Não foi possivel popular o db, certifique-se que as migrations foram rodadas")
