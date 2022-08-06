from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

from .utils import tabela_orientandos, linhas_grafico, tabela_ultimas_publicações, pizza

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





def docentes(request):
    tabela = tabela_orientandos()
    grafico_ori = pizza()
    linhas = linhas_grafico()
    tabela_publi = tabela_ultimas_publicações()


    docente = [
        {
            'nome' : 'Vladimir Safatle',
            'programa' : 'Filosofia',
            'departamento' : 'Filosofia'
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
            'ano' : 'Ano'
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