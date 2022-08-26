from unicodedata import name
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot

from .apis import Api



class Departamentos():

    def __init__(self):
        pass 


    def tabela_todos_docentes(self):
        api = Api()
        dados = api.pega_dados_docentes()
        #dados_programas = api.pega_dados_programas_docentes()


        df = pd.DataFrame(dados)
        df = df.drop(columns=['codset'])
        #df2 = pd.DataFrame(dados_programas['departamentos'])

        #x = 0
        #siglas_codigos = {}
       # while x < 11:
        #    siglas_codigos[df2.iloc[x]['sigla']] = df2.iloc[x]['codigo']
            
        #    x += 1

        

        #lista_valores = df.values.tolist()

        titulo = 'Todos os docentes da faculdade'
        return df, titulo


