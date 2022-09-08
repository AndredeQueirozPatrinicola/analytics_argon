from unicodedata import name
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from plotly.offline import plot


class Grafico():

    def plota(self, fig):

        graph = plot(fig, output_type="div", config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        return graph

    def grafico_pizza(self, *args, **kwargs):
        # values
        # names
        # colors
        # color_discrete_sequence
        # labels
        # height
        # margin

        values = kwargs.get('values')
        names = kwargs.get('names')
        color = kwargs.get('color')
        color_discrete_sequence = kwargs.get('color_discrete_sequence')
        height = kwargs.get('height')
        x = kwargs.get('x')
        y = kwargs.get('y')
        legend_orientation = kwargs.get('legend_orientation')
        labels = kwargs.get('labels')
        margin = kwargs.get('margin')

        fig = px.pie(values=values, names=names, color=color,
                     color_discrete_sequence=color_discrete_sequence, height=height, labels=labels)

        fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', },
                          margin=margin, legend=dict(orientation=legend_orientation, yanchor="bottom", y=y, xanchor="right", x=x))

        grafico = self.plota(fig)

        return grafico

    def grafico_linhas(self, *args, **kwargs):
        # df ou nao
        # x
        # y
        # colors
        # color_discrete_sequence
        # barmode
        # labels
        # height
        # margin
        # line,grid color

        df = kwargs.get('df')
        color = kwargs.get('color')
        color_discrete_sequence = kwargs.get('color_discrete_sequence')
        height = kwargs.get('height')
        x = kwargs.get('x')
        y = kwargs.get('y')
        legend_orientation = kwargs.get('legend_orientation')
        labels = kwargs.get('labels')
        margin = kwargs.get('margin')
        font_color = kwargs.get('font_color')
        showlegend = kwargs.get('showlegend')

        fig = px.line(df, x=x, y=y, height=height, labels=labels,
                      color=color, color_discrete_sequence=color_discrete_sequence)
        
        fig.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        }, margin=margin, font_color=font_color, showlegend=showlegend)

        fig.update_layout(autosize=True)
        fig.update_xaxes(showline=True, linewidth=1, linecolor='white',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#4d4b46', automargin=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white',
                         mirror=True, showgrid=True, gridwidth=1, gridcolor='#4d4b46', automargin=True)

        grafico = self.plota(fig)

        return grafico

    def grafico_barras():
        # df ou nao
        # x
        # y
        # colors
        # color_discrete_sequence
        # barmode
        # labels
        # height
        # margin
        # line,grid color

        pass
