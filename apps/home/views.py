from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

import requests
import pandas as pd

from .utils import Docente

def index(request):
    context = {
        'segment': 'index',
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))





def docentes(request, parametro):
    docente = Docente(parametro)


    tabela = docente.tabela_orientandos()
    grafico_ori = docente.plota_pizza()
    linhas = docente.plota_grafico_historico()
    tabela_publi = docente.tabela_ultimas_publicações()


    docente = [
        {
            'nome' : docente.dados.get('nome'),
            'programa' : '',
            'departamento' : '',
            'link_lattes': 'http://lattes.cnpq.br/' + docente.dados.get('id_lattes')
        }
    ]


    grafico_pizza_titulo = [
        {
            'titulo' : 'Relação entre mestrandos e doutorandos'
        }
    ]
    
    grafico_titulo = [
        {
            'titulo' : 'Produção de artigos por ano (2000 - 2021)',
            'categoria' : 'Artigos'
        }
    ]

    tabela_header = [
        {
            'titulo' : 'Orientandos Ativos',
            'nome' : 'Nome',
            'nivel' : 'Nivel',
            'programa' : 'Programa'
        }
    ]

    tabela_publicacoes = [
        {
            'titulo' : 'Ultimas publicações',
            'titulo_trabalho' : 'Titulo',
            'ano' : 'Ano de publicação'
        }
    ]

    caminho = [
        {
            'text' :"Departamentos", 
            'url' : "/"
        },
        {
            'text' : "Docentes",
            'url' : '/docentes/'
        }
    ]

    context = {
        'tabela_header' : tabela_header,
        'caminho' : caminho,
        'tabela' : tabela,
        'grafico_ori' : grafico_ori,
        'tabela_pu' : tabela_publi,
        'tabela_publicacoes' : tabela_publicacoes,
        'linhas' : linhas,
        'grafico_titulo' : grafico_titulo,
        'grafico_pizza_titulo' : grafico_pizza_titulo,
        'docente' : docente
    }

    return render(request, 'home/docentes.html', context)


def departamento(request, sigla):

    api = requests.get('https://dados.fflch.usp.br/api/programas')
    dados = api.json()

    for i in dados['departamentos']:
        if i['sigla'] == sigla:
            nome = i['nome']
            id = i['id_lattes_docentes']
            codset = i['codigo']

    docentes_api = requests.get('https://dados.fflch.usp.br/api/docentes')
    dados_docentes = docentes_api.json()

    docentes = []

    for docente in dados_docentes:
        if int(docente['codset']) == int(codset):
            docentes.append(docente)

    df = pd.DataFrame(docentes)

    id_lattes = df['id_lattes']

    caminho = [
        {
            'text' : nome,
            'url' : '/departamento/' + sigla
        }
    ]

    context = {
        'caminho' : caminho,
        'nome' : nome,
        'id_lattes' : id,
        'docentes' : docentes,
        'df' : df,
        'lattes_id' : id_lattes
    }

    return render(request, 'home/departamento.html', context)