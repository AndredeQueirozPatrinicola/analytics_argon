import requests
from time import sleep

from apps.home.models import Departamento



api = 'https://dados.fflch.usp.br/api/'

class Api:

    def __init__(self):
        self.api = api
        self.api_programas = self.api + 'programas/'
        self.api_docentes = self.api + 'docentes'
        self.api_programas_docentes = self.api_programas + 'docente/'
        self.api_pesquisa = self.api + 'pesquisa'


    def pega_dados_departamentos(self):
        siglas = ['FLA', 'FLP', 'FLF', 'FLH', 'FLC', 'FLM', 'FLO', 'FLL', 'FSL', 'FLT', 'FLG']
        anos = [2016,2017,2018,2019,2020,2021]

        departamentos_siglas = {'FLA': 'Antropologia', 'FLP': 'Ciência Política', 'FLF': 'Filosofia', 'FLH': 'História', 'FLC': "Letras Clássicas e Vernáculas",
                                'FLM': "Letras Modernas", 'FLO': 'Letras Orientais', 'FLL': 'Lingüística', 'FSL': 'Sociologia', 'FLT': "Teoria Literária e Literatura Comparada", 'FLG': 'Geografia'}

        parametros = {
            'filtro' : 'serie_historica',
            'ano_ini' : 2016,
            'ano_fim' : 2021,
            'serie_historica_tipo' : 'departamento'
        }
        
        parametros_vazios = {
            'filtro' : 'departamento',
            'ano_ini' : '',
            'ano_fim' : '',
            'serie_historica_tipo' : ''
        }

        raw_programas = requests.get('https://dados.fflch.usp.br/api/programas')
        raw_docentes = requests.get('https://dados.fflch.usp.br/api/docentes')
        raw_pesquisa = requests.get(url='https://dados.fflch.usp.br/api/pesquisa', params=parametros_vazios)
        raw_pesquisa_parametros = requests.get(url = f'https://dados.fflch.usp.br/api/pesquisa', params=parametros)



        dados_programas = raw_programas.json() # dicionario com dicionarios # FEITO
        dados_docentes = raw_docentes.json()   # lista com dicionarios # FEITO
        dados_pesquisa = raw_pesquisa.json()   # dicionarios com dicionario  FEITO
        dados_pesquisa_parametros = raw_pesquisa_parametros.json() #dicionarios com dicionarios

        x = 0
        while x < len(siglas):
                
                
            # Dicionario com dados de pesquisa por departamento
            siglas_dic = {siglas[x] : dados_pesquisa.get(siglas[x])}
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
                    # Resultado a ser salvo
                    lista_programas_departamentos = [i]

                z += 1
            
            
            
            # Bloco que pega dados dos anos 2016 - 2021 sobre produção 
            y = 0
            lista_programas_docentes = []
            while y < len(anos):
                sleep(1)
                parametros_programas = {'tipo' : 'anual', 'ano' : anos[y], 'ano_ini' : '', 'ano_fim' : ''}

                print(anos[y])
                raw_programas_docentes = requests.get(
                    url=f'https://dados.fflch.usp.br/api/programas/docentes/{siglas[x]}', params=parametros_programas)

                dados_programas_docentes = raw_programas_docentes.json()  # FEITO

                # Lista com dados da produção de todos os docentes por ano (2016-2021)
                dicionario_dados = {anos[y]: dados_programas_docentes}
                lista_programas_docentes.append(dicionario_dados)
                
            
                y += 1

                
                
            dados = [siglas_dic, 
            lista_programas_docentes, 
            lista_programas_departamentos, 
            lista_pesquisa_por_ano, 
            dados_docentes_filtrados]



            dados = Departamento(sigla = siglas[x], 
                                api_docentes=dados_docentes_filtrados,
                                api_programas=lista_programas_departamentos, 
                                api_programas_docente=lista_programas_docentes,
                                api_pesquisa=siglas_dic, 
                                api_pesquisa_parametros = lista_pesquisa_por_ano)
            
            dados.save()

            x += 1


if __name__ == "__main__":
    api = Api()
    api.pega_dados_departamentos()