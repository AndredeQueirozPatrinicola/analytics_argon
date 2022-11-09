import requests
import os, django
import pandas as pd
from time import sleep
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.utils import Utils
from apps.home.models import Departamento, Docente, Mapa


class ApiDepartamento:

    def __init__(self, sigla: str) -> None:
        self.sigla = sigla

    def pega_api_docentes(self):
        utils = Utils()
        dados_docentes = requests.get('https://dados.fflch.usp.br/api/docentes')
        dados_docentes = dados_docentes.json() 
        departamentos_siglas = utils.siglas_departamentos('departamentos')
        dados_docentes = [i for i in dados_docentes if i.get('nomset') == departamentos_siglas.get(self.sigla)]

        return dados_docentes

    def pega_api_programas(self):
        dados_programas = requests.get('https://dados.fflch.usp.br/api/programas')
        dados_programas = dados_programas.json()
        dados_programas = dados_programas.get('departamentos')
        x = 0
        for i in dados_programas:
            if dados_programas[x].get('sigla') == self.sigla:
                lista_programas_departamentos = [i]
            x += 1

        return lista_programas_departamentos

    def pega_api_pesquisa_vazio(self):
        parametros_vazios = {
            'filtro': 'departamento',
            'ano_ini': '',
            'ano_fim': '',
            'serie_historica_tipo': ''
        }
        dados_pesquisa = requests.get(url='https://dados.fflch.usp.br/api/pesquisa', params=parametros_vazios)
        dados_pesquisa = dados_pesquisa.json()   
        dados_pesquisa = {self.sigla: dados_pesquisa.get(self.sigla)}
        
        return dados_pesquisa

    def pega_api_pesquisa_parametros(self):
        departamentos_siglas = Utils()
        departamentos_siglas = departamentos_siglas.siglas_departamentos('departamentos')
        parametros = {
            'filtro': 'serie_historica',
            'ano_ini': 2016,
            'ano_fim': 2021,
            'serie_historica_tipo': 'departamento'
        }
        raw_pesquisa_parametros = requests.get(url=f'https://dados.fflch.usp.br/api/pesquisa', params=parametros)
        dados_pesquisa_parametros = raw_pesquisa_parametros.json()

        for i in dados_pesquisa_parametros:
                if i == departamentos_siglas.get(self.sigla):
                    lista_pesquisa_por_ano = [dados_pesquisa_parametros.get(i)]

        return lista_pesquisa_por_ano

    def pega_api_defesas(self):
        def get_key(val):
                for key, value in utils.dptos_programas.items():
                    if val == value:
                        return key

        raw_defesas = requests.get('https://dados.fflch.usp.br/api/defesas')
        dados_defesas = raw_defesas.json()
        utils = Utils()

        # Lista com dicionarios
        dados_api_defesas = []
        for i in dados_defesas:  
            codare = dados_defesas[dados_defesas.index(i)].get('codare')
            for j in utils.dptos_programas:    
                dptm = utils.dptos_programas.get(self.sigla)
                if codare in dptm:
                    regulador = get_key(dptm)
                    if regulador == self.sigla:
                        dados_api_defesas.append(dados_defesas[dados_defesas.index(i)])


        return dados_api_defesas

    def pega_api_programas_docentes(self):
        anos = [int(i) for i in range(datetime.now().year - 6, datetime.now().year)]
        y = 0
        lista_programas_docentes = []
        while y < len(anos):
            sleep(1)
            parametros_programas = {
                'tipo': 'anual', 'ano': anos[y], 'ano_ini': '', 'ano_fim': ''}

            try:
                raw_programas_docentes = requests.get(
                    url=f'https://dados.fflch.usp.br/api/programas/docentes/{self.sigla}', params=parametros_programas)
                print(f"{anos[y]} - {y + 1}/{len(anos)}")
            except:
                print("Houve um problema na requisição de dados das APIs")
                raise Exception()

            dados_programas_docentes = raw_programas_docentes.json()  

            # Lista com dados da produção de todos os docentes por ano (2016-2021)
            dicionario_dados = {str(anos[y]): dados_programas_docentes}
            lista_programas_docentes.append(dicionario_dados)

            y += 1

        return lista_programas_docentes

    def pega_api_programas_docentes_limpo(self):

        x = 0
        while x < len(self.sigla):

            try:
                raw_programas_docente_limpo = requests.get(f'https://dados.fflch.usp.br/api/programas/docentes/{self.sigla}')
                dados_programas_docentes_limpo = raw_programas_docente_limpo.json()
                api_programas_docentes_limpo = dados_programas_docentes_limpo
            except:
                print("Houve um problema na requisição de dados das APIs")
                raise Exception()

            x += 1

        return api_programas_docentes_limpo

    def atualiza_ou_cria_departamento(self, api_docentes, api_programas, api_pesquisa_vazio, api_pesquisa_parametros,api_defesas,api_programas_docentes,api_programas_docentes_limpo):
        departamento = Departamento.objects.filter(sigla=self.sigla)

        if departamento.exists():

            departamento.update(
                api_docentes=api_docentes,
                api_programas=api_programas, 
                api_pesquisa=api_pesquisa_vazio, 
                api_pesquisa_parametros=api_pesquisa_parametros, 
                api_defesas=api_defesas, 
                api_programas_docente=api_programas_docentes, 
                api_programas_docente_limpo=api_programas_docentes_limpo, 
            )

        else:
            departamento = Departamento(
                api_docentes=api_docentes,
                api_programas=api_programas, 
                api_pesquisa=api_pesquisa_vazio, 
                api_pesquisa_parametros=api_pesquisa_parametros, 
                api_defesas=api_defesas, 
                api_programas_docente=api_programas_docentes, 
                api_programas_docente_limpo=api_programas_docentes_limpo, 
            )

            departamento.save()