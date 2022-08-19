import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

API = 'https://dados.fflch.usp.br/api/'
API_PROGRAMAS = API + 'programas/'
API_DOCENTES = API + 'docentes'
API_PROGRAMAS_DOCENTE = API_PROGRAMAS + 'docente/'


class Departamento():

    def __init__(self, sigla):
        res = requests.get(url=API_PROGRAMAS)
        dados = res.json()
        res_docentes = requests.get(url=API_DOCENTES)
        dados_docentes = res_docentes.json()
        self.dados_docentes = dados_docentes
        self.dados = dados
        self.sigla = sigla

    def tabela_docentes(self, sigla):
        dados = self.dados
        dados_docentes = self.dados_docentes

        for i in dados['departamentos']:
            if i['sigla'] == sigla:
                nome = i['nome']
                id = i['id_lattes_docentes']
                codset = i['codigo']

        docentes = [i for i in dados_docentes if int(
            i['codset']) == int(codset)]

        df = pd.DataFrame(docentes)

        id_lattes = df['id_lattes']

        return df, id_lattes, nome, id
