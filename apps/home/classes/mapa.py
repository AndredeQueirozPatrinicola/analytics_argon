import plotly.graph_objects as go
from plotly.offline import plot
import requests
import plotly.express as px
import pandas as pd
import os
from time import sleep

from apps.home.utils import Utils

class Mapa:

    def __init__(self):
        pass 


    def plota_mapa():
        fig = go.Figure(go.Scattergeo(lat=[], lon=[]))
        fig = fig.update_geos(showcountries=True, projection_type="orthographic",
                        projection_rotation=dict(lon=-56, lat=-13), )
        fig = fig.update_layout(height=550, margin={"r": 0, "t": 0, "l": 0, "b": 2})

        fig = plot(fig, output_type="div", config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        return fig

    def plota_mapa_v2(self):
        """
            Metodo que visita uma base de dados dos estados brasileiros no Github e os 
            dados dos alunos na api e retorna o mapa plotado junto com o numero de alunos
            de São Paulo. 

            Em caso de erro neste processo, retorna mensagem de erro que será exibida no front.
        """
        pd.options.mode.chained_assignment = None

        response_base_dados = requests.get(url = 'https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json')
        response_api = requests.get(url = 'https://dados.fflch.usp.br/api/alunosAtivosEstado')

        if response_base_dados.status_code == 200 and response_api.status_code == 200:
            state_geo = response_base_dados.json()
            state_data = response_api.json()

            estados = Utils()
            estados = estados.pega_codigo_estado()

            state_data = pd.DataFrame(state_data, index=[0])
            state_data = state_data.drop('', axis=1)
            state_data = state_data.transpose()
            state_data = state_data.rename(columns={0:"Alunos"})
            state_data = state_data.sort_index(ascending=True)
            state_data['Codigos'] = [estados.get(i) for i in estados]
            state_data['UFs'] = [i for i in state_data.index]
            state_data.index = [i for i in range(0,len(state_data.index))]
            quantidade_alunos_sp = state_data['Alunos'][25]
            state_data['Alunos'][25] = 0
            state_data.to_csv('apps/static/assets/csv/data.csv')
            state_data = pd.read_csv('apps/static/assets/csv/data.csv')

            if os.path.exists('apps/static/assets/csv/data.csv'):
                os.remove('apps/static/assets/csv/data.csv')

            quantidade_alunos_sp = str(quantidade_alunos_sp)
            numero = quantidade_alunos_sp[-3]
            quantidade_alunos_sp = quantidade_alunos_sp.split(quantidade_alunos_sp[-3])
            quantidade_alunos_sp = quantidade_alunos_sp[0] + "." + numero + quantidade_alunos_sp[1]

            fig = px.choropleth(
                                state_data, 
                                geojson=state_geo, 
                                color="Alunos",
                                locations="Codigos", 
                                featureidkey="properties.GEOCODIGO",
                                projection="orthographic",
                                color_continuous_scale="PuBu",
                                title='Alunos da FFLCH fora de São Paulo',
                                labels={
                                    'Alunos':'Alunos', 
                                    "Codigos" : "Codigo da UF"
                                    },
                                )

            fig.update_geos(fitbounds="geojson", visible=False)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

            fig = plot(fig, output_type="div", config={
                                                        'displaylogo': False,
                                                        'modeBarButtonsToRemove': [
                                                            'select2d', 'lasso2d', 
                                                            'select', 'zoomIn', 
                                                            'zoomOut', 'autoScale', 
                                                            'resetScale', 'zoom', 
                                                            'pan', 'toImage'
                                                            ]})

            return fig, quantidade_alunos_sp
        # except:
        #     erro = "Houve um problema para fornecer o gráfico"
        #     return erro
            


            