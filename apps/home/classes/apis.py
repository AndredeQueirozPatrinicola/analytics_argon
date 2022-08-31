import requests



api = 'https://dados.fflch.usp.br/api/'



class Api:

    def __init__(self):
        self.api = api
        self.api_programas = self.api + 'programas/'
        self.api_docentes = self.api + 'docentes'
        self.api_programas_docentes = self.api_programas + 'docentes/'
        self.api_programas_docente = self.api_programas + 'docente/'
        self.api_pesquisa = self.api + 'pesquisa'


    def pega_dados_programas(self): # 1 2
        res = requests.get(url=self.api_programas)
        dados = res.json()
        return dados

    def pega_dados_docentes(self): # 1 2 3
        res = requests.get(url=self.api_docentes)
        dados = res.json()
        return dados

    def pega_dados_programas_docentes(self, sigla): #  1 2
        res = requests.get(url=self.api_programas_docentes + sigla)
        dados = res.json()
        return dados


    def pega_dados_programas_docente(self, parametro): #  1 2
        res = requests.get(url=self.api_programas_docente + parametro)
        dados = res.json()
        return dados


    def pega_dados_pesquisa(self, *args): # 1 2 

        if args == ():
            res = requests.get(url=self.api_pesquisa, params='filtro=departamento&ano_ini=&ano_fim=&serie_historica_tipo=')
            dados = res.json()
            return dados
        else:
            parametros = {
                'filtro' : args[0],
                'ano_ini' : args[1],
                'ano_fim' : args[2],
                'serie_historica_tipo' : args[3]
            }

            res = requests.get(url=self.api_pesquisa, params=parametros)
            dados = res.json()
            return dados