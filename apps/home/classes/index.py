from plotly.offline import plot
import plotly.express as px
import pandas as pd
import os
import locale
from functools import cached_property

from apps.home.utils import Utils
from apps.home.models import Mapa


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

    @cached_property
    def dados_mapa(self):
        try:
            dados_alunos = self.__mapa_quantidade_alunos_estado_dados[0].get('dados_do_mapa')
            dados_alunos = pd.DataFrame([dados_alunos])
            try:
                dados_alunos.loc[0, 'RR']
            except:
                dados_alunos['RR'] = 0
            dados_alunos = dados_alunos.transpose()
            dados_alunos = dados_alunos.rename(columns={0:"Alunos"}, index={"":"Não Informado"})
            dados_alunos = dados_alunos.sort_index(ascending=True)

            return dados_alunos
        except:
            raise Exception()

    def regula_escala(self, valor):
        valor = valor + 50
        escala = int(valor/9)
        return [i for i in range(0,escala*10, escala)]

    def plota_mapa(self):
        """
            Metodo que visita uma base de dados dos estados brasileiros no Github e os 
            dados dos alunos na api e retorna o mapa plotado junto com o numero de alunos
            de São Paulo. 

            Em caso de erro neste processo, retorna mensagem de erro que será exibida no front.
        """
        pd.options.mode.chained_assignment = None

        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            state_geo = self.__mapa_quantidade_alunos_estado_base[0].get('base_de_dados')

            estados = Utils().pega_codigo_estado()
            df_estados = pd.DataFrame([estados])
            df_estados = df_estados.transpose()
            df_estados = df_estados.rename(columns={0:"Codigos"})

            dados_alunos = self.dados_mapa

            df_merged = dados_alunos.join(df_estados)
            df_merged['Codigos'] = df_merged['Codigos'].fillna(0)
            df_merged['Codigos'] = df_merged['Codigos'].apply(int)

            df_merged.to_csv('apps/static/assets/csv/data.csv')
            df_merged = pd.read_csv('apps/static/assets/csv/data.csv')

            if os.path.exists('apps/static/assets/csv/data.csv'):
                os.remove('apps/static/assets/csv/data.csv')
            
            escala_numerica_grafico = self.regula_escala(df_merged['Alunos'].nlargest(2).tolist()[1])
            escala_string_legenda = [str(i) for i in escala_numerica_grafico]
            escala_string_legenda[-1] = ">" + escala_string_legenda[-1]

            fig = px.choropleth(
                                df_merged, 
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
                                range_color=[escala_numerica_grafico[0], escala_numerica_grafico[-1]]
                                )

            fig.update_geos(fitbounds="geojson", visible=True)
            fig.update_layout(
                                margin={"r":0,"t":0,"l":0,"b":0},
                                coloraxis_colorbar=dict(
                                title="Legenda(Nº de pessoas)",
                                tickvals=escala_numerica_grafico,
                                ticktext=escala_string_legenda
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

            return fig 
        except:
            return None
            

    def tabela_alunos_estados(self):
        try:
            data = self.dados_mapa
            siglas = data.index.to_list()
            quantidade = data['Alunos'].to_list()

            tabela = []
            x = 0
            while x < len(siglas)/2:
                tabela.append([siglas[x], quantidade[x], siglas[x+14], quantidade[x+14]])
                x+=1

            return {
                'headers': ["Siglas", "Valores", "Siglas", "Valores"],
                'tabelas' : tabela
            }
        except:
            erro = [["Houve um problema para fornecer a tabela"]]
            return erro


            