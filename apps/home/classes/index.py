from plotly.offline import plot
import plotly.express as px
import pandas as pd
import os
import locale

from apps.home.utils import Utils
from apps.home.models import Mapa

from django.utils.formats import localize

class Index:

    def __init__(self):
        self.__mapa_quantidade_alunos_estado_base = Mapa.objects.filter(nome="MapaIndexAlunos").values('base_de_dados')
        self.__mapa_quantidade_alunos_estado_dados = Mapa.objects.filter(nome="MapaIndexAlunos").values('dados_do_mapa')
      

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
        try:
            dados_api = self.__mapa_quantidade_alunos_estado_dados[0].get('dados_do_mapa')
            dados_api = pd.DataFrame(dados_api, index=[0])
            dados_api = dados_api.drop('', axis=1)
            dados_api = dados_api.transpose()
            dados_api = dados_api.rename(columns={0:"Alunos"})

            return dados_api
        except:
            raise Exception()

    def plota_mapa(self):
        # """
        #     Metodo que visita uma base de dados dos estados brasileiros no Github e os 
        #     dados dos alunos na api e retorna o mapa plotado junto com o numero de alunos
        #     de São Paulo. 

        #     Em caso de erro neste processo, retorna mensagem de erro que será exibida no front.
        # """
            pd.options.mode.chained_assignment = None

        # try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            estados = Utils()
            estados = estados.pega_codigo_estado()
            state_geo = self.__mapa_quantidade_alunos_estado_base[0].get('base_de_dados')

            state_data = self._trata_dados_api()
            state_data = state_data.sort_index(ascending=True)
            state_data['Codigos'] = [estados.get(i) for i in estados]
            state_data['UFs'] = [i for i in state_data.index]
            state_data.index = [i for i in range(0,len(state_data.index))]
            quantidade_alunos_sp = state_data['Alunos'][25]
            state_data.to_csv('apps/static/assets/csv/data.csv')
            state_data = pd.read_csv('apps/static/assets/csv/data.csv')

            if os.path.exists('apps/static/assets/csv/data.csv'):
                os.remove('apps/static/assets/csv/data.csv')
            
            quantidade_alunos_sp = int(quantidade_alunos_sp) / 1000
            quantidade_alunos_sp = round(quantidade_alunos_sp, 3)

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
                                range_color=[0, 400]
                                )

            fig.update_geos(fitbounds="geojson", visible=False)
            fig.update_layout(
                                margin={"r":0,"t":0,"l":0,"b":0},
                                coloraxis_colorbar=dict(
                                title="Escala",
                                tickvals=[0, 50, 100, 150, 200, 250, 300, 350, 400],
                                ticktext=[
                                    "0", 
                                    "50",
                                    "100",
                                    "150",
                                    "200",
                                    "250",
                                    "300",
                                    "350",
                                    ">400"

                                ],
                            ))

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
        #     return None
            

    def tabela_alunos_estados(self):
        try:
            data = self._trata_dados_api()
            estados = data.index.to_list()
            alunos = data["Alunos"].to_list()

            x = 0
            resultado = [] 
            while x < len(estados)/2 + 0.5:
                try:
                    resultado.append([estados[x], alunos[x], estados[x + 14], alunos[x + 14]])
                except:
                    resultado.append([estados[x], alunos[x], '    -   ', '      -   '])
                x += 1

            return resultado
        except:
            erro = [["Houve um problema para fornecer a tabela"]]
            return erro


            