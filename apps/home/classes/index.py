import plotly.graph_objects as go
from plotly.offline import plot
import requests
import plotly.express as px
import pandas as pd
import os
from time import sleep

from apps.home.utils import Utils
from apps.home.models import Mapa

class Index:

    def __init__(self):
        self.mapa_quantidade_alunos_estado_base = Mapa.objects.filter(nome="MapaIndexAlunos").values('base_de_dados')
        self.mapa_quantidade_alunos_estado_dados = Mapa.objects.filter(nome="MapaIndexAlunos").values('dados_do_mapa')
      

    def tabela_sobrenos(self):
        titulo = 'FFLCH | Analytics'
        menu_nav_table = [
            {
                'titulo': 'Sobre nós',

                'text1': 'Sobre o projeto',

                'text2': 'Portal de dados',

                'text3': 'Escritório de apoio institucional ao pesquisador - EAIP | FFLCH'
            }
        ]
        return menu_nav_table, titulo

    def _trata_dados_api(self):
        # try:
            state_data = self.mapa_quantidade_alunos_estado_dados[0].get('dados_do_mapa')

            state_data = pd.DataFrame(state_data, index=[0])
            state_data = state_data.drop('', axis=1)
            state_data = state_data.transpose()
            state_data = state_data.rename(columns={0:"Alunos"})

            return state_data
        # except:
        #     raise Exception()

    def plota_mapa(self):
        """
            Metodo que visita uma base de dados dos estados brasileiros no Github e os 
            dados dos alunos na api e retorna o mapa plotado junto com o numero de alunos
            de São Paulo. 

            Em caso de erro neste processo, retorna mensagem de erro que será exibida no front.
        """
        pd.options.mode.chained_assignment = None

        try:
                estados = Utils()
                estados = estados.pega_codigo_estado()
                state_geo = self.mapa_quantidade_alunos_estado_base[0].get('base_de_dados')

                state_data = self._trata_dados_api()
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
                                    height=680,
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
        except:
            erro = "Houve um problema para fornecer o gráfico"
            return erro
            

    def tabela_alunos_estados(self):
        data = self._trata_dados_api()
        estados = data.index.to_list()
        alunos = data["Alunos"].to_list()

        x = 0
        resultado = [] 
        while x < len(estados):
            
            resultado.append([estados[x], alunos[x]])
            
            x += 1
            
        return resultado


            