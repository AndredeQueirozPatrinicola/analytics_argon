import requests

from .models import Departamento, Docente

from time import sleep

api = 'https://dados.fflch.usp.br/api/'


class Api:

    def __init__(self):
        self.api = api
        self.api_programas = self.api + 'programas/'
        self.api_docentes = self.api + 'docentes'
        self.api_programas_docentes = self.api_programas + 'docente/'
        self.api_pesquisa = self.api + 'pesquisa'

    def pega_dados_programas(self):

        siglas = ['FLA', 'FLP', 'FLF', 'FLH', 'FLC', 'FLM', 'FLO', 'FLL', 'FSL', 'FLT', 'FLG']
        anos = [2016,2017,2018,2019,2020,2021]

        parametros_vazios = {
            'filtro' : 'departamento',
            'ano_ini' : '',
            'ano_fim' : '',
            'serie_historica_tipo' : ''
        }

        parametros = {
            'filtro' : 'serie_historica',
            'ano_ini' : 2016,
            'ano_fim' : 2021,
            'serie_historica_tipo' : 'departamento'
        }

        raw_programas = requests.get('https://dados.fflch.usp.br/api/programas')
        raw_docentes = requests.get('https://dados.fflch.usp.br/api/docentes')
        raw_pesquisa = requests.get(url='https://dados.fflch.usp.br/api/pesquisa', params=parametros_vazios)
        raw_pesquisa_parametros = requests.get(url = f'https://dados.fflch.usp.br/api/pesquisa', params=parametros)


        dados_programas = raw_programas.json() # dicionario com dicionarios
        dados_docentes = raw_docentes.json()   # lista com dicionarios
        dados_pesquisa = raw_pesquisa.json()   # dicionarios com dicionario
        dados_pesquisa_parametros = raw_pesquisa_parametros() #dicionarios com dicionarios
        
        c = 0
        lista_programas_docentes = []
        while c < len(anos):
            parametros_programas = {'tipo' : 'periodo', 'ano_ini' : anos[c], 'ano_fim' : 2021}

            raw_programas_docentes = requests.get(url=f'https://dados.fflch.usp.br/api/programas/docentes/{siglas[c]}', params=parametros_programas)
        
            dados_programas_docentes = raw_programas_docentes.json()  

            lista_programas_docentes.append(dados_programas_docentes)
        
        
        
        
        
        
        departamentos_siglas = {'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Linguística', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}



        
        
        siglas_dic = {}
        x = 0
        while x < len(siglas):
            siglas_dic[siglas[x]] = dados_pesquisa.get(siglas[x])

        # siglas_dic -> dados_pesquisa ex:{'FLA':{dados:dados} }










    def pega_dados_docente(self):
        print('oi')
        response = requests.get('https://dados.fflch.usp.br/api/programas')
        data = response.json()


        api_departamentos = [i for i in data.get('departamentos')]
        api_programas = [i for i in data.get('programas')]



        g = 0
        lista_id_docentes = []
        while g < len(api_programas):
            teste = api_programas[g].get('docentes')
            lista_id_docentes.append(teste)
            
            g += 1



        g = 0
        lista_id_docentes_dep = []
        while g < len(api_departamentos):
            teste = api_departamentos[g].get('id_lattes_docentes')
            lista_id_docentes_dep.append(teste)
            
            g += 1



        for i in lista_id_docentes:
            x = 0
            lista_id_docentes[x].sort()
            x += 1
            
            
        for j in lista_id_docentes_dep:
            c = 0
            lista_id_docentes[c].sort()
            c += 1


        lista_id_docentes_reta = [item for sublist in lista_id_docentes for item in sublist]
        lista_id_docentes_dep_reta = [item for sublist in lista_id_docentes_dep for item in sublist]
        lista = [lista_id_docentes_reta, lista_id_docentes_dep_reta]
        parametros = [item for sublist in lista for item in sublist]
        parametros = [*set(parametros)]


        for i in parametros:
            if i == None:
                parametros.remove(i)

        z = 0
        while z < len(parametros):
            sleep(4)
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
                
                verifica = Docente.objects.filter(docente_id=parametros[z])

                verifica.update(api_programas=lista_api)
                



            #salva_json = Docente(docente_id=parametro,
                                   # api_docente=docentes_dados, api_programas=lista_api)


            z += 1

            #salva_json.save()
