from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

import requests
import pandas as pd

#from .utils import Docente, Departamento

from .classes.docente import Docente
from .classes.departamento import Departamento

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





def docente(request, sigla, parametro):
    docente = Docente(parametro, sigla)

    tabela = docente.tabela_orientandos()
    grafico_ori = docente.plota_grafico_pizza()
    grafico_artigos, grafico_titulo_artigos = docente.plota_grafico_historico('artigos')
    grafico_livros, grafico_titulo_livros = docente.plota_grafico_historico('livros')
    grafico_capitulos, grafico_titulo_capitulos = docente.plota_grafico_historico('capitulos')
    tabela_publi = docente.tabela_ultimas_publicacoes()
    caminho = docente.pega_caminho()
    titulo_linhas, linhas_pesquisa = docente.linhas_de_pesquisa()

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


    context = {
        'tabela_header' : tabela_header,
        'caminho' : caminho,
        'tabela' : tabela,
        'grafico_ori' : grafico_ori,
        'tabela_pu' : tabela_publi,
        'tabela_publicacoes' : tabela_publicacoes,
        'grafico_artigos' : grafico_artigos,
        'grafico_titulo_artigos' : grafico_titulo_artigos,
        'grafico_livros' : grafico_livros,
        'grafico_titulo_livros' : grafico_titulo_livros,
        'grafico_pizza_titulo' : grafico_pizza_titulo,
        'grafico_capitulos' : grafico_capitulos,
        'grafico_titulo_capitulos' : grafico_titulo_capitulos,
        'docente' : docente,
        'sigla_departamento' : sigla,
        'linhas_pesquisa' : linhas_pesquisa,
        'titulo_linhas' : titulo_linhas
    }

    return render(request, 'home/docentes.html', context)


def docentes(request, sigla):
    
    docentes = Departamento(sigla)

    df, id_lattes, nome, id = docentes.tabela_docentes(sigla)
    numero_docentes = docentes.pega_numero_docentes(sigla)
    grafico_pizza_aposentados_ativos, titulo_aposentados_ativos = docentes.plota_aposentados_ativos(sigla)
    grafico_pizza_tipo_vinculo, titulo_tipo_vinculo = docentes.plota_tipo_vinculo_docente(sigla)



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
        'lattes_id' : id_lattes,
        'tabela' : 'docentes',
        'sigla_departamento' : sigla,
        'numero_docentes' : numero_docentes,
        'grafico_aposentados_ativos' : grafico_pizza_aposentados_ativos,
        'titulo_aposentados_ativos' : titulo_aposentados_ativos,
        'grafico_tipo_vinculo' : grafico_pizza_tipo_vinculo,
        'titulo_tipo_vinculo' : titulo_tipo_vinculo
    }

    return render(request, 'home/departamento.html', context)



def departamentos(request):



    return render(request, 'home/departamentos.html')


