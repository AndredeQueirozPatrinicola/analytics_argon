import plotly.graph_objects as go
from plotly.offline import plot
import requests
import plotly.express as px
import pandas as pd

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

    def plota_mapa_v2():
        pd.options.mode.chained_assignment = None
        #Insumo 1: GeoJSON dos estados brasileiros
        response = requests.get(url = 'https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json')
        if response.status_code == 200: # O código 200 (OK) indica que a solicitação foi bem sucedida
            state_geo = response.json()

        response = requests.get('https://dados.fflch.usp.br/api/alunosAtivosEstado')
        if response.status_code == 200:
            state_data = response.json()
            state_data = pd.DataFrame(state_data, index=[0])

        state_data = state_data.drop('', axis=1)
        state_data = state_data.transpose()
        state_data = state_data.rename(columns={0:"Alunos"})
        state_data = state_data.sort_index(ascending=True)
        estados = Utils.pega_codigo_estado()
        state_data['Codigos'] = [estados.get(i) for i in estados]
        state_data['UFs'] = [i for i in state_data.index]
        state_data.index = [i for i in range(0,len(state_data.index))]
        quantidade_alunos_sp = state_data['Alunos'][25]
        state_data['Alunos'][25] = 0 
        state_data.to_csv('data.csv')
        state_data = pd.read_csv('data.csv')

        quantidade_alunos_sp = str(quantidade_alunos_sp)
        numero = quantidade_alunos_sp[-3]
        quantidade_alunos_sp = quantidade_alunos_sp.split(quantidade_alunos_sp[-3])
        quantidade_alunos_sp = quantidade_alunos_sp[0] + "." + numero + quantidade_alunos_sp[1]

        fig = px.choropleth(state_data, geojson=state_geo, color="Alunos",
                    locations="Codigos", featureidkey="properties.GEOCODIGO",
                    projection="orthographic",
                    color_continuous_scale="PuBu",
                    title='Alunos da FFLCH fora de São Paulo',
                    labels={'Alunos':'Alunos', "Codigos" : "Codigo da UF"},
                   )
        fig.update_geos(fitbounds="geojson", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        fig = plot(fig, output_type="div", config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        return fig, quantidade_alunos_sp