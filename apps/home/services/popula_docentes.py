import requests
from time import sleep

from apps.home.models import Docente




api = 'https://dados.fflch.usp.br/api/'

class Api:

    def __init__(self):
        self.api = api
        self.api_programas = self.api + 'programas/'
        self.api_docentes = self.api + 'docentes'
        self.api_programas_docentes = self.api_programas + 'docente/'
        self.api_pesquisa = self.api + 'pesquisa'


    def popula_docentes(self):
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

        print('oi')
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
                
                #verifica = Docente.objects.filter(docente_id=parametros[z])

                #verifica.update(api_programas=lista_api)
                

            print('oi3')

            salva_json = Docente(docente_id=parametro,
                                    api_docente=docentes_dados, api_programas=lista_api)

            salva_json.save()
            print('oila')
            z += 1



if __name__ == "__main__":
    api = Api()
    api.popula_docentes()