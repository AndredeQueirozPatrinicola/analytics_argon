import requests
import os, django
import pandas as pd
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.models import Departamento, Docente


api = 'https://dados.fflch.usp.br/api/'

class Api:

    def __init__(self):
        self.api = api
        self.api_programas = self.api + 'programas/'
        self.api_docentes = self.api + 'docentes'
        self.api_programas_docentes = self.api_programas + 'docente/'
        self.api_pesquisa = self.api + 'pesquisa'

    def pega_dados_departamentos(self):
        print("Checando Apis...")

        numero_total_mudanças = 0

        siglas = ['FLA', 'FLP', 'FLF', 'FLH', 'FLC',
                  'FLM', 'FLO', 'FLL', 'FSL', 'FLT', 'FLG']
        anos = [2016, 2017, 2018, 2019, 2020, 2021]

        departamentos_siglas = {
            'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
            'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Lingüística', 'FSL': 'Sociologia', 
            'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'
            }

        parametros = {
            'filtro': 'serie_historica',
            'ano_ini': 2016,
            'ano_fim': 2021,
            'serie_historica_tipo': 'departamento'
        }

        parametros_vazios = {
            'filtro': 'departamento',
            'ano_ini': '',
            'ano_fim': '',
            'serie_historica_tipo': ''
        }

        raw_programas = requests.get(
            'https://dados.fflch.usp.br/api/programas')
        raw_docentes = requests.get('https://dados.fflch.usp.br/api/docentes')
        raw_pesquisa = requests.get(
            url='https://dados.fflch.usp.br/api/pesquisa', params=parametros_vazios)
        raw_pesquisa_parametros = requests.get(
            url=f'https://dados.fflch.usp.br/api/pesquisa', params=parametros)

        dados_programas = raw_programas.json()  
        dados_docentes = raw_docentes.json()   
        dados_pesquisa = raw_pesquisa.json()   
        dados_pesquisa_parametros = raw_pesquisa_parametros.json()

        x = 0
        while x < len(siglas):

            raw_programas_docente_limpo = requests.get(
                f'https://dados.fflch.usp.br/api/programas/docentes/{siglas[x]}')
            dados_programas_docentes_limpo = raw_programas_docente_limpo.json()
            api_programas_docentes_limpo = dados_programas_docentes_limpo

            # Dicionario com dados de pesquisa por departamento
            dados_pesquisa_tratados = {siglas[x]: dados_pesquisa.get(siglas[x])}
            print(siglas[x])

            # Lista com dicionario com dados dos docentes de cada departamento
            dados_docentes_filtrados = [i for i in dados_docentes if i.get(
                'nomset') == departamentos_siglas.get(siglas[x])]

            # Lista com dicionarios por ano
            for i in dados_pesquisa_parametros:
                if i == departamentos_siglas.get(siglas[x]):
                    lista_pesquisa_por_ano = [dados_pesquisa_parametros.get(i)]

            # Lista de dicionarios com os dados por departamento da api de programas
            dados_dep = dados_programas.get('departamentos')
            z = 0
            for i in dados_dep:
                if dados_dep[z].get('sigla') == siglas[x]:
                    lista_programas_departamentos = [i]

                z += 1

            # Bloco que pega dados dos anos 2016 - 2021 sobre produção
            y = 0
            lista_programas_docentes = []
            while y < len(anos):
                sleep(1)
                parametros_programas = {
                    'tipo': 'anual', 'ano': anos[y], 'ano_ini': '', 'ano_fim': ''}

                print(f"Dados de {anos[y]} salvos")
                raw_programas_docentes = requests.get(
                    url=f'https://dados.fflch.usp.br/api/programas/docentes/{siglas[x]}', params=parametros_programas)

                dados_programas_docentes = raw_programas_docentes.json()  

                # Lista com dados da produção de todos os docentes por ano (2016-2021)
                dicionario_dados = {str(anos[y]): dados_programas_docentes}
                lista_programas_docentes.append(dicionario_dados)

                y += 1


            verifica_api_docentes = Departamento.objects.filter(sigla = siglas[x]).values_list('api_docentes')
            verifica_api_programas = Departamento.objects.filter(sigla = siglas[x]).values_list('api_programas')
            verifica_programas_docente = Departamento.objects.filter(sigla = siglas[x]).values_list('api_programas_docente')
            verifica_api_pesquisa = Departamento.objects.filter(sigla = siglas[x]).values_list('api_pesquisa')
            verifica_api_pesquisa_parametros = Departamento.objects.filter(sigla = siglas[x]).values_list('api_pesquisa_parametros')
            verifica_api_programas_docente_limpo = Departamento.objects.filter(sigla = siglas[x]).values_list('api_programas_docente_limpo')

            verifica_existencia = Departamento.objects.filter(sigla=siglas[x])

            verifica_mudanca = False

            if verifica_existencia.exists():

                if verifica_api_docentes[0][0] != dados_docentes_filtrados:
                    print("Api docentes com diferença")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_docentes=dados_docentes_filtrados)

                if verifica_api_programas[0][0] != lista_programas_departamentos:
                    print("Api programas com diferença")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_programas=lista_programas_departamentos)
                
                if verifica_programas_docente[0][0] != lista_programas_docentes:
                    print("Api programas docente com diferença")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_programas_docente=lista_programas_docentes)
                
                if verifica_api_pesquisa[0][0] != dados_pesquisa_tratados:
                    print("Api pesquisa com diferença")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_pesquisa=dados_pesquisa_tratados)

                if verifica_api_pesquisa_parametros[0][0] != lista_pesquisa_por_ano:
                    print("Api pesquisa por ano com diferença")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_pesquisa_parametros=lista_pesquisa_por_ano)

                if verifica_api_programas_docente_limpo[0][0] != api_programas_docentes_limpo:
                    print("Api programas docente limpo com diferença")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_programas_docente_limpo=api_programas_docentes_limpo)


                if verifica_mudanca == True:
                    print(f"{siglas[x]} atualizado com sucesso")

                else:
                    print(f"{siglas[x]} não teve mudanças")

            else:
                dados = Departamento(sigla=siglas[x],
                                     api_docentes=dados_docentes_filtrados,
                                     api_programas=lista_programas_departamentos,
                                     api_programas_docente=lista_programas_docentes,
                                     api_pesquisa=dados_pesquisa_tratados,
                                     api_pesquisa_parametros=lista_pesquisa_por_ano,
                                     api_programas_docente_limpo=api_programas_docentes_limpo)

                dados.save()
                print(f"{siglas[x]} salvo com sucesso")

            x += 1
        
        print(f"Houveram {numero_total_mudanças} mudanças")

    def pega_dados_docente(self):
        print("Checando Apis...")

        numero_total_mudanças = 0

        res = requests.get('https://dados.fflch.usp.br/api/docentes')
        dados = res.json()
        df = pd.DataFrame(dados)
        parametros = df['id_lattes'].to_list()
        parametros = [i for i in parametros if i != "0"]

        z = 0
        while z < len(parametros):
            sleep(2)
            parametro = parametros[z]

            docentes = requests.get(
                url=self.api_programas_docentes + parametro)
            programas = requests.get(url=self.api_programas)

            docentes_dados = docentes.json()
            programas_dados = programas.json()

            dados_departamentos = programas_dados['departamentos']
            dados_programas = programas_dados['programas']

            x = 0
            lista_api = []
            while x < len(dados_departamentos):
                if parametro in dados_departamentos[x].get('id_lattes_docentes'):
                    lista_api.append(dados_departamentos[x])

                x += 1

            if lista_api == []:
                lista_api.append(dados_programas) 
            
            for i in dados: 
                if i.get('id_lattes') == parametros[z]:
                    dados_api_docentes = i



            verifica_api_docente = Docente.objects.filter(docente_id=parametros[z]).values_list('api_docente')
            verifica_api_programas = Docente.objects.filter(docente_id=parametros[z]).values_list('api_programas')
            verifica_api_docentes = Docente.objects.filter(docente_id=parametros[z]).values_list('api_docentes')

            verifica_existencia = Docente.objects.filter(docente_id = parametros[z])

            verifica_mudanca = False

            if verifica_existencia.exists() and parametros[z] != "0":

                if docentes_dados != verifica_api_docente[0][0]:
                    print("Api docente: Atualizada!")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    verifica_api_docente = Docente.objects.filter(docente_id=parametros[z]).update(api_docente=docentes_dados)

                if lista_api != verifica_api_programas[0][0]:
                    print("Api programas: Atualizada!")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    verifica_api_docente = Docente.objects.filter(docente_id=parametros[z]).update(api_programas=lista_api)

                if dados_api_docentes != verifica_api_docentes[0][0]:
                    print("Api docentes: Atualizada!")
                    verifica_mudanca = True
                    numero_total_mudanças += 1
                    verifica_api_docente = Docente.objects.filter(docente_id=parametros[z]).update(api_docentes=dados_api_docentes)


                if verifica_mudanca == True:
                    print(f'Atualizou: {parametros[z]} | {z+1} de {len(parametros)}')
                else:
                    print(f"Sem mudanças: {parametros[z]} | {z+1} de {len(parametros)}")

            else:
                salva_json = Docente(docente_id=parametro,
                                    api_docente=docentes_dados, 
                                    api_programas=lista_api, 
                                    api_docentes=dados_api_docentes)

                salva_json.save()
                print(f'Salvou: {parametros[z]} | {z+1} de {len(parametros)}')

            z += 1

        print(f"Houveram {numero_total_mudanças} mudanças")



if __name__ == '__main__':
    api = Api()
    api.pega_dados_departamentos()
    api.pega_dados_docente()
    print('Banco de dados populado com sucesso')