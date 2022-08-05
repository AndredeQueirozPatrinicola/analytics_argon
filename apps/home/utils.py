import numpy as np
import pandas as pd
import requests
import plotly.express as px
from plotly.offline import plot


# Utils

def tabela_orientandos():
    res = requests.get(url = 'https://dados.fflch.usp.br/api/programas/docente/7208476340192177')
    dados = res.json()
    df = pd.DataFrame(dados['orientandos'])

    nomep = list(df['nompes'])
    nivpgm = list(df['nivpgm'])
    nomare = list(df['nomare'])

    lis = []
    x = 0
    while x < len(nomep):
        lis.append([f'{nomep[x]}', f'{nivpgm[x]}' , f'{nomare[x]}'])
        x += 1

    return lis


def pizza():
    res = requests.get(url = 'https://dados.fflch.usp.br/api/programas/docente/7208476340192177')
    dados = res.json()
    df = pd.DataFrame(dados['orientandos'])

    nivpgm = list(df['nivpgm'])
    tipos = ['ME', 'DO']

    nivel = []
    x,y = 0, 0
    for i in nivpgm:
        if i == 'ME':
            x += 1
        if i == 'DO':
            y += 1

    nivel.append(x)
    nivel.append(y)        

    figura = px.pie(values=nivel, names=tipos, width=450, color=tipos, color_discrete_sequence=["#052e70", "#AFAFAF"], labels={
        'values': 'Valor',
        'names': 'Tipo',
        'color' : 'Cor'
    })

    figura.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
        l=60, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))


    grafico_pizza = plot(figura, output_type='div', config={
    'displaylogo': False,
    'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

    return grafico_pizza



def linhas_grafico():
    res = requests.get(
        url='https://dados.fflch.usp.br/api/programas/docente/7208476340192177')
    dados = res.json()

    artigos = dados.get('artigos')
    df_artigos = pd.DataFrame(artigos)

    ano = df_artigos['ANO'].value_counts()
    ano_sortado = ano.sort_index(ascending=True)
    df_ano_artigos = pd.DataFrame(ano_sortado)
    eixo_x = df_ano_artigos.index

    linhas = px.line(df_ano_artigos, x=eixo_x, y='ANO', width=980, height=400, labels={
        'index': '',
        'ANO': ''
    })

    linhas.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
        l=20, r=20, t=20, b=50), font_color="white", showlegend=False)
    linhas.update_xaxes(showline=True, linewidth=1, linecolor='white',
                        mirror=True, showgrid=True, gridwidth=1, gridcolor='grey')
    linhas.update_yaxes(showline=True, linewidth=1, linecolor='white',
                        mirror=True, showgrid=True, gridwidth=1, gridcolor='grey')

    graph = plot(linhas, output_type="div", config={
        'displaylogo': False,
        'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

    return graph


def tabela_ultimas_publicações():
    res = requests.get(url = 'https://dados.fflch.usp.br/api/programas/docente/7208476340192177')
    dados = res.json()
    tabela = pd.DataFrame(dados['livros'])
    publicacoes = tabela.head(5)
    titulo_ano = publicacoes[['TITULO-DO-LIVRO', 'ANO']]
    publicacao_com_ano = titulo_ano.values.tolist()

    return publicacao_com_ano