import plotly.express as px
from plotly.offline import plot


class Grafico():

    def plota(self, fig):

        graph = plot(fig, output_type="div", config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d','select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

        return graph

    def grafico_pizza(self, *args, **kwargs):

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

    def grafico_barras(self, *args, **kwargs):

        df = kwargs.get('df')
        color = kwargs.get('color')
        color_discrete_sequence = kwargs.get('color_discrete_sequence')
        color_discrete_map = kwargs.get('color_discrete_map')
        height = kwargs.get('height')
        x = kwargs.get('x')
        y = kwargs.get('y')
        legend_orientation = kwargs.get('legend_orientation')
        labels = kwargs.get('labels')
        margin = kwargs.get('margin')
        font_color = kwargs.get('font_color')
        showlegend = kwargs.get('showlegend')
        barmode = kwargs.get('barmode')
        legend = kwargs.get('legend')
        bargroupgap = kwargs.get('bargroupgap')
        bargap = kwargs.get('bargap')
        autosize = kwargs.get('autosize')
        yaxis_title = kwargs.get('yaxis_title')
        linecolor = kwargs.get('linecolor')
        gridcolor = kwargs.get('gridcolor')

        if barmode:
            fig = px.bar(df, x=x, y=y,
                                height=height, color=color, color_discrete_sequence=color_discrete_sequence, color_discrete_map=color_discrete_map,
                            labels=labels, barmode=barmode)
        else:
            fig = px.bar(df, x=x, y=y,
                    height=height, color=color, color_discrete_sequence=color_discrete_sequence, color_discrete_map=color_discrete_map,
                labels=labels)


        fig.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        }, margin=margin, showlegend=showlegend,font_color=font_color, legend=legend, bargroupgap=bargroupgap, bargap=bargap, autosize=autosize, yaxis_title=yaxis_title)

        fig.update_xaxes(showline=True, linewidth=1, linecolor=linecolor,
                         mirror=True, showgrid=True, gridwidth=1, gridcolor=gridcolor, automargin=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor=linecolor,
                         mirror=True, showgrid=True, gridwidth=1, gridcolor=gridcolor, automargin=True)

        grafico = self.plota(fig)

        return grafico