import plotly.graph_objects as go
from plotly.offline import plot



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