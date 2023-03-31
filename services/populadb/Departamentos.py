import requests
import os, django
from time import sleep
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.utils import Utils
from apps.home.models import Departamento


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
            'ano_ini': datetime.now().year - 6,
            'ano_fim': datetime.now().year - 1,
            'serie_historica_tipo': 'departamento'
        }
        dados_pesquisa_parametros = requests.get(url=f'https://dados.fflch.usp.br/api/pesquisa', params=parametros)
        dados_pesquisa_parametros = dados_pesquisa_parametros.json()

        resultado = dados_pesquisa_parametros.get(departamentos_siglas.get(self.sigla))

        if not resultado:
            resultado = dados_pesquisa_parametros.get('Linguística')
        
        return resultado

    def pega_api_defesas(self):
        utils = Utils()
        ano_atual = datetime.now().year - 1
        api_defesas = requests.get(f'https://dados.fflch.usp.br/api/defesas?ano={ano_atual}&codcur=')
        api_defesas = api_defesas.json()

        defesas = []
        for defesa in api_defesas:

            codigo_programa = defesa.get('codare')  
            programa_para_departamento = utils.pega_departamento_programa(codigo_programa)

            if programa_para_departamento.get('sigla') == self.sigla:
                defesas.append(defesa)

        return defesas



    def pega_api_programas_docentes(self):
        anos = [int(i) for i in range(datetime.now().year - 6, datetime.now().year)]
        y = 0
        lista_programas_docentes = []
        while y < len(anos):
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

    def atualiza_ou_cria_departamento(self, sigla, api_docentes, api_programas, api_pesquisa_vazio, api_pesquisa_parametros,api_defesas,api_programas_docentes,api_programas_docentes_limpo):
        departamento = Departamento.objects.filter(sigla=self.sigla)

        if departamento.exists():
            departamento.update(
                sigla=sigla,
                api_docentes=api_docentes,
                api_programas=api_programas, 
                api_pesquisa=api_pesquisa_vazio, 
                api_pesquisa_parametros=api_pesquisa_parametros, 
                api_defesas=api_defesas, 
                api_programas_docente=api_programas_docentes, 
                api_programas_docente_limpo=api_programas_docentes_limpo, 
            )
            print("Dados atualizados com sucesso")
        else:
            departamento = Departamento(
                sigla=sigla,
                api_docentes=api_docentes,
                api_programas=api_programas, 
                api_pesquisa=api_pesquisa_vazio, 
                api_pesquisa_parametros=api_pesquisa_parametros, 
                api_defesas=api_defesas, 
                api_programas_docente=api_programas_docentes, 
                api_programas_docente_limpo=api_programas_docentes_limpo, 
            )
            print("Departamento salvo com sucesso")
            departamento.save()