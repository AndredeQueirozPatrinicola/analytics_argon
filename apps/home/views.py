from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

from apps.home.models import Docente

from .classes.docente import DadosDocente
from .classes.departamento import DadosDepartamento
from .classes.departamentos import Departamentos


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

    docente = DadosDocente(parametro, sigla)

    tabela_orientandos, tabela_header = docente.tabela_orientandos()
    grafico_mestre_dout, titulo_mestr_dout = docente.plota_grafico_pizza()
    grafico_artigos, grafico_titulo_artigos = docente.plota_grafico_historico('artigos')
    grafico_livros, grafico_titulo_livros = docente.plota_grafico_historico('livros')
    grafico_capitulos, grafico_titulo_capitulos = docente.plota_grafico_historico('capitulos')
    tabela_publicacoes, titulo_publicacoes = docente.tabela_ultimas_publicacoes()
    caminho = docente.pega_caminho()
    titulo_linhas, linhas_pesquisa = docente.linhas_de_pesquisa()

    docente = [
        {
            'nome' : caminho[1].get('text'),
            'programa' : '',
            'departamento' : '',
            'link_lattes': 'http://lattes.cnpq.br/' + parametro
        }
    ]

    context = {
        'caminho' : caminho,

        'tabela' : tabela_orientandos,
        'tabela_header' : tabela_header,

        'grafico_ori' : grafico_mestre_dout,
        'grafico_pizza_titulo' : titulo_mestr_dout,

        'tabela_pu' : tabela_publicacoes,
        'tabela_publicacoes' : titulo_publicacoes,

        'grafico_artigos' : grafico_artigos,
        'grafico_titulo_artigos' : grafico_titulo_artigos,

        'grafico_livros' : grafico_livros,
        'grafico_titulo_livros' : grafico_titulo_livros,

        'grafico_capitulos' : grafico_capitulos,
        'grafico_titulo_capitulos' : grafico_titulo_capitulos,

        'docente' : docente,

        'sigla_departamento' : sigla,
        
        'linhas_pesquisa' : linhas_pesquisa,
        'titulo_linhas' : titulo_linhas,


    }

    return render(request, 'home/docentes.html', context)


def departamento(request, sigla):
    
    docentes = DadosDepartamento(sigla)

    df, id_lattes, nome, id = docentes.tabela_docentes(sigla)
    numero_docentes = docentes.pega_numero_docentes(sigla)
    grafico_pizza_aposentados_ativos, titulo_aposentados_ativos = docentes.plota_aposentados_ativos(sigla)
    grafico_pizza_tipo_vinculo, titulo_tipo_vinculo = docentes.plota_tipo_vinculo_docente(sigla)
    grafico_prod_docentes, titulo_prod_docentes = docentes.plota_prod_departamento(sigla)
    grafico_historico_prod, titulo_historico_prod = docentes.plota_prod_serie_historica(sigla)
    grafico_bolsas, titulo_bolsas = docentes.plota_grafico_bolsa_sem()
    tabela_bolsas, titulo_tabela_bolsas  = docentes.tabela_trabalhos(sigla)

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
        'titulo_tipo_vinculo' : titulo_tipo_vinculo,

        'grafico_prod_docentes' : grafico_prod_docentes, 
        'titulo_prod_docentes' : titulo_prod_docentes,

        'tabela_bolsas' : tabela_bolsas,
        'titulo_tabela_bolsas' : titulo_tabela_bolsas,

        'grafico_bolsas' : grafico_bolsas,
        'titulo_bolsas': titulo_bolsas,

        'grafico_historico_prod' : grafico_historico_prod,
        'titulo_historico_prod' : titulo_historico_prod

    }

    return render(request, 'home/departamento.html', context)



def departamentos(request):
    departamentos = Departamentos()

    df_docentes, titulo_tabela_todos_docentes = departamentos.tabela_todos_docentes()
    grafico_relacao_cursos, titulo_relacao_cursos = departamentos.plota_relacao_cursos()

    grafico_bolsas, titulo_grafico_bolsas = departamentos.grafico_bolsa_sem()

    tabela_bolsas, titulo_tabela_bolsas = departamentos.tabela_trabalhos()

    grafico_prod, titulo_prod = departamentos.prod_total_departamentos()

    

    context = {
        'df_docentes' : df_docentes,
        'titulo_tabela_todos_docentes' : titulo_tabela_todos_docentes,
        'grafico_relacao_cursos' :  grafico_relacao_cursos,
        'titulo_relacao_cursos' : titulo_relacao_cursos,
        'grafico_bolsas' : grafico_bolsas,
        'titulo_bolsas' : titulo_grafico_bolsas,
        'tabela_bolsas' : tabela_bolsas,
        'titulo_tabela_bolsas' : titulo_tabela_bolsas,
        'grafico_prod_docentes' : grafico_prod,
        'titulo_prod_docentes' : titulo_prod
    }


    return render(request, 'home/departamentos.html', context)



def testes(request):
    parametro = '9156992025883151'

    teste = Docente.objects.filter(docente_id=parametro).values_list()

    teste = teste[0][2]

    context = {
        'teste' : teste
    }

    return render(request, 'home/testes.html', context)






