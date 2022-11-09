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

class PopulaDB:

    def __init__(self):
        self.api = api
        self.api_programas = self.api + 'programas/'
        self.api_docentes = self.api + 'docentes'
        self.api_programas_docentes = self.api_programas + 'docente/'
        self.api_pesquisa = self.api + 'pesquisa'

    def pega_dados_departamentos(self):
        print("Checando Apis...")

        numero_total_mudancas = 0

        programas_dpto = {
                'FLP' : [8131],
                'FSL' : [8132],
                'FLF' : [8133],
                'FLA' : [8134],
                'FLG' : [8135, 8136],
                'FLH' : [8137, 8138],
                'FLL' : [8139],
                'FLC' : [8142, 8143, 8149, 8150, 8156, 8162],
                'FLM' : [8144, 8145, 8146, 8147, 8148, 8158, 8160, 8163, 8164, 8165],
                'FLT' : [8151],
                'FLO' : [8155, 8157],
        }

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

        try:
            raw_programas = requests.get('https://dados.fflch.usp.br/api/programas')
            raw_docentes = requests.get('https://dados.fflch.usp.br/api/docentes')
            raw_pesquisa = requests.get(url='https://dados.fflch.usp.br/api/pesquisa', params=parametros_vazios)
            raw_pesquisa_parametros = requests.get(url=f'https://dados.fflch.usp.br/api/pesquisa', params=parametros)
            raw_defesas = requests.get('https://dados.fflch.usp.br/api/defesas')
        
        except:
            print("Houve um problema na requisição de dados das APIs")
            raise Exception()

        dados_programas = raw_programas.json()  
        dados_docentes = raw_docentes.json()   
        dados_pesquisa = raw_pesquisa.json()   
        dados_pesquisa_parametros = raw_pesquisa_parametros.json()
        dados_defesas = raw_defesas.json()
        

        x = 0
        while x < len(siglas):

            try:
                raw_programas_docente_limpo = requests.get(f'https://dados.fflch.usp.br/api/programas/docentes/{siglas[x]}')
                
                dados_programas_docentes_limpo = raw_programas_docente_limpo.json()
                api_programas_docentes_limpo = dados_programas_docentes_limpo

            except:
                print("Houve um problema na requisição de dados das APIs")
                raise Exception()



            def get_key(val):
                for key, value in programas_dpto.items():
                    if val == value:
                        return key

            # Lista com dicionarios
            dados_api_defesas = []
            for i in dados_defesas:  
                codare = dados_defesas[dados_defesas.index(i)].get('codare')
                for j in programas_dpto:    
                    dptm = programas_dpto.get(siglas[siglas.index(j)])
                    if codare in dptm:
                        regulador = get_key(dptm)
                        if regulador == siglas[x]:
                            dados_api_defesas.append(dados_defesas[dados_defesas.index(i)])

            
            # Dicionario com dados de pesquisa por departamento
            dados_pesquisa_tratados = {siglas[x]: dados_pesquisa.get(siglas[x])}
            print(siglas[x])

            # Lista com dicionario com dados dos docentes de cada departamento
            dados_docentes_filtrados = [i for i in dados_docentes if i.get('nomset') == departamentos_siglas.get(siglas[x])]

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

                try:
                    raw_programas_docentes = requests.get(
                        url=f'https://dados.fflch.usp.br/api/programas/docentes/{siglas[x]}', params=parametros_programas)
                    print(f"{anos[y]} - {y + 1}/{len(anos)}")
                except:
                    print("Houve um problema na requisição de dados das APIs")
                    raise Exception()

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
            verifica_api_defesas = Departamento.objects.filter(sigla = siglas[x]).values_list('api_defesas')

            verifica_existencia = Departamento.objects.filter(sigla=siglas[x])

            verifica_mudanca = False

            if verifica_existencia.exists():

                if verifica_api_docentes[0][0] != dados_docentes_filtrados:
                    print("Api docentes com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_docentes=dados_docentes_filtrados)

                if verifica_api_programas[0][0] != lista_programas_departamentos:
                    print("Api programas com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_programas=lista_programas_departamentos)
                
                if verifica_programas_docente[0][0] != lista_programas_docentes:
                    print("Api programas docente com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_programas_docente=lista_programas_docentes)
                
                if verifica_api_pesquisa[0][0] != dados_pesquisa_tratados:
                    print("Api pesquisa com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_pesquisa=dados_pesquisa_tratados)

                if verifica_api_pesquisa_parametros[0][0] != lista_pesquisa_por_ano:
                    print("Api pesquisa por ano com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_pesquisa_parametros=lista_pesquisa_por_ano)

                if verifica_api_programas_docente_limpo[0][0] != api_programas_docentes_limpo:
                    print("Api programas docente limpo com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_programas_docente_limpo=api_programas_docentes_limpo)

                if verifica_api_defesas[0][0] != dados_api_defesas:
                    print("Api defesas com diferença")
                    verifica_mudanca = True
                    numero_total_mudancas += 1
                    Departamento.objects.filter(sigla=siglas[x]).update(api_defesas=dados_api_defesas)


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
                                     api_programas_docente_limpo=api_programas_docentes_limpo,
                                     api_defesas=dados_api_defesas)

                dados.save()
                print(f"{siglas[x]} salvo com sucesso")

            x += 1
        
        print(f"Houveram {numero_total_mudancas} mudanças")

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

            docentes = requests.get(url=self.api_programas_docentes + parametro)
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


class PopulaDB2():

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


    def informacoes_dps(self):
        programas_dpto = {
            'FLP' : [8131],
            'FSL' : [8132],
            'FLF' : [8133],
            'FLA' : [8134],
            'FLG' : [8135, 8136],
            'FLH' : [8137, 8138],
            'FLL' : [8139],
            'FLC' : [8142, 8143, 8149, 8150, 8156, 8162],
            'FLM' : [8144, 8145, 8146, 8147, 8148, 8158, 8160, 8163, 8164, 8165],
            'FLT' : [8151],
            'FLO' : [8155, 8157],
        }

        siglas = ['FLA', 'FLP', 'FLF', 'FLH', 'FLC', 'FLM', 'FLO', 'FLL', 'FSL', 'FLT', 'FLG']

        anos = [2016, 2017, 2018, 2019, 2020, 2021]

        


if __name__ == '__main__':
    api = PopulaDB()
    api2 = PopulaDB2()
    utils = Utils()

    try:
        numeros_usp = api2.pega_numeros_usp()
        print("Começando a popular tabela de docentes")
        for numero_usp in numeros_usp:

            indice = numeros_usp.index(numero_usp)

            docente = ApiDocente(numero_usp)
            dados_api_docente = docente.pega_api_docente()
            dados_api_programas = docente.pega_api_programas()
            dados_api_docentes = docente.pega_api_docentes()

            docente.atualiza_ou_cria_docente(dados_api_docente, dados_api_programas, dados_api_docentes)
            print(f"Docente {numero_usp} salvo ou atualizado. {indice + 1}/{len(numeros_usp)}")
            sleep(2)

        siglas_departamentos = utils.siglas_departamentos('siglas')
        print("Começando a popular tabela de departamentos")
        for sigla in siglas_departamentos:
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

            # api.pega_dados_departamentos()
            # api.pega_dados_docente()
        api.pega_dados_mapas()
        print('Banco de dados populado com sucesso')
    except:
        print("Não foi possivel popular o db, certifique-se que as migrations foram rodadas")


