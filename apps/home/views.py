from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

from apps.home.models import Docente, Departamento

from .classes.docente import DadosDocente
from .classes.departamento import DadosDepartamento
from .classes.departamentos import Departamentos
from .classes.index import Index


def pages(request):
    context = {}
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

class IndexView(View):

    def get(self, request):
        titulo_destaques = 'Destaques'
        destaques = [

            """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            """,

            """
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            """
        ]
        index = Index()
        try:
            globo, quantidade_alunos_sp = index.plota_mapa()
        except:
            globo = index.plota_mapa()
            quantidade_alunos_sp = None

        menu_nav_table, titulo_menu = index.tabela_sobrenos()
        tabela_alunos_estados = index.tabela_alunos_estados()

        context = {
            'segment': 'index',
            'landingpage': 'landingpage',

            'titulo': titulo_menu,
            'menu_table': menu_nav_table,

            'globo': globo,
            'quantidade_alunos_sp' : quantidade_alunos_sp,
            'tabela_alunos_estados' : tabela_alunos_estados,

            'titulo_destaques' : titulo_destaques,
            'destaques' : destaques
        }

        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
class DocenteView(View):

    def queries(self, parametro):
        querie = Docente.objects.filter(docente_id=parametro).values()
        querie = querie[0]

        api_docente = querie.get('api_docente')
        api_programas = querie.get('api_programas')
        api_docentes = querie.get('api_docentes')

        return api_docente, api_programas, api_docentes

    def get(self, request, sigla, parametro):
        try:
            docente = DadosDocente(parametro, sigla)
            api_docente, api_programas, api_docentes = self.queries(parametro)

            tabela_orientandos, tabela_header = docente.tabela_orientandos(api_docente)
            grafico_mestre_dout, titulo_mestr_dout = docente.plota_grafico_pizza(api_docente)
            grafico_artigos, grafico_titulo_artigos = docente.plota_grafico_historico('artigos', api_docente)
            grafico_livros, grafico_titulo_livros = docente.plota_grafico_historico('livros', api_docente)
            grafico_capitulos, grafico_titulo_capitulos = docente.plota_grafico_historico('capitulos', api_docente)
            tabela_publicacoes, titulo_publicacoes = docente.tabela_ultimas_publicacoes(api_docente)
            caminho = docente.pega_caminho(api_programas, api_docentes)
            label_dropdown, linhas_pesquisa = docente.linhas_de_pesquisa(api_docente)
            tipo_vinculo, situacao = docente.pega_vinculo_situacao(api_docentes)

            docente = [
                {
                    'nome': caminho[1].get('text'),
                    'programa': '',
                    'departamento': '',
                    'link_lattes': 'http://lattes.cnpq.br/' + parametro
                }
            ]

            context = {
                'caminho': caminho,

                'tabela': tabela_orientandos,
                'tabela_header': tabela_header,

                'grafico_ori': grafico_mestre_dout,
                'grafico_pizza_titulo': titulo_mestr_dout,

                'tabela_pu': tabela_publicacoes,
                'tabela_publicacoes': titulo_publicacoes,

                'grafico_artigos': grafico_artigos,
                'grafico_titulo_artigos': grafico_titulo_artigos,

                'grafico_livros': grafico_livros,
                'grafico_titulo_livros': grafico_titulo_livros,

                'grafico_capitulos': grafico_capitulos,
                'grafico_titulo_capitulos': grafico_titulo_capitulos,

                'docente': docente,  # card 1
                'card_1_titulo': 'Nome / Lattes',

                'sigla_departamento': sigla,

                'informacoes_card': linhas_pesquisa,  # card 2
                'dropdown_label': label_dropdown,
                'card_2_titulo': 'Linhas de pesquisa',  # card 2

                'card_3': tipo_vinculo,  # card 3
                'card_3_titulo': 'Tipo de vínculo',

                'card_4': situacao,  # card 4
                'card_4_titulo': 'Situação atual',

            }

            return render(request, 'home/docentes.html', context)
        except:
            context = {}
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))

class DepartamentoView(View):
    
    def queries(self, sigla):
        querie = Departamento.objects.filter(sigla=sigla).values()
        querie = querie[0]

        api_docentes = querie.get('api_docentes')
        api_programas = querie.get('api_programas')
        api_programas_docente = querie.get('api_programas_docente')
        api_pesquisa = querie.get('api_pesquisa')
        api_pesquisa_parametros = querie.get('api_pesquisa_parametros')
        api_programas_docente_limpo = querie.get('api_programas_docente_limpo')
        api_defesas = querie.get('api_defesas')

        return api_docentes, api_programas, api_programas_docente, api_pesquisa, api_pesquisa_parametros, api_programas_docente_limpo, api_defesas
    
    def get(self, request, sigla):
        try:
            docentes = DadosDepartamento(sigla)

            api_docentes, api_programas, api_programas_docente, api_pesquisa, api_pesquisa_parametros, api_programas_docente_limpo, api_defesas = self.queries(sigla)

            df, id_lattes, nome, id = docentes.tabela_docentes(api_programas, api_docentes)
            numero_docentes, x, y, z = docentes.pega_numero_docentes(api_programas, api_docentes)
            grafico_pizza_aposentados_ativos, titulo_aposentados_ativos = docentes.plota_aposentados_ativos(api_programas, api_docentes)
            grafico_pizza_tipo_vinculo, titulo_tipo_vinculo = docentes.plota_tipo_vinculo_docente(api_docentes)
            grafico_prod_docentes, titulo_prod_docentes = docentes.plota_prod_departamento(api_programas_docente_limpo)
            grafico_historico_prod, titulo_historico_prod = docentes.plota_prod_serie_historica(api_programas_docente)
            grafico_bolsas, titulo_bolsas = docentes.plota_grafico_bolsa_sem(api_pesquisa_parametros)
            tabela_bolsas, titulo_tabela_bolsas = docentes.tabela_trabalhos(api_pesquisa)
            programas_dpto, label_dropdown = docentes.pega_programa_departamento()

            caminho = [
                {
                    'text': nome,
                    'url': '/departamento/' + sigla
                }
            ]

            context = {
                'regulador': 'regulador',

                'caminho': caminho,
                'nome': nome,

                'id_lattes': id,
                'docentes': docentes,
                'df': df,
                'lattes_id': id_lattes,
                'tabela': 'docentes',
                'sigla_departamento': sigla,

                'numero_docentes': numero_docentes,

                'grafico_aposentados_ativos': grafico_pizza_aposentados_ativos,
                'titulo_aposentados_ativos': titulo_aposentados_ativos,

                'grafico_tipo_vinculo': grafico_pizza_tipo_vinculo,
                'titulo_tipo_vinculo': titulo_tipo_vinculo,

                'grafico_prod_docentes': grafico_prod_docentes,
                'titulo_prod_docentes': titulo_prod_docentes,

                'tabela_bolsas': tabela_bolsas,
                'titulo_tabela_bolsas': titulo_tabela_bolsas,

                'grafico_bolsas': grafico_bolsas,
                'titulo_bolsas': titulo_bolsas,

                'grafico_historico_prod': grafico_historico_prod,
                'titulo_historico_prod': titulo_historico_prod,

                'informacoes_card': programas_dpto,
                'dropdown_label': label_dropdown,
                'card_2_titulo': 'Programas do departamento'

            }

            return render(request, 'home/departamento.html', context)

        except:
            context = {}
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))


class DepartamentosView(View):

    def queries(self):
        pass

    def get(self, request):
        departamentos = Departamentos()
        try:
            df_docentes, titulo_tabela_todos_docentes = departamentos.tabela_todos_docentes()
            grafico_relacao_cursos, titulo_relacao_cursos = departamentos.plota_relacao_cursos()
            grafico_bolsas, titulo_grafico_bolsas = departamentos.grafico_bolsa_sem()
            tabela_bolsas, titulo_tabela_bolsas = departamentos.tabela_trabalhos()
            grafico_prod, titulo_prod = departamentos.prod_total_departamentos()
            grafico_prod_historico, titulo_prod_historico = departamentos.prod_historica_total()
            numero_docentes = departamentos.pega_numero_docentes()
            programas_departamento, dropdown_label = departamentos.pega_programas()

            caminho = [
                {
                    'text': 'Departamentos',
                }
            ]

            context = {
                'caminho': caminho,

                'df_docentes': df_docentes,
                'titulo_tabela_todos_docentes': titulo_tabela_todos_docentes,

                'grafico_relacao_cursos':  grafico_relacao_cursos,
                'titulo_relacao_cursos': titulo_relacao_cursos,

                'grafico_bolsas': grafico_bolsas,
                'titulo_bolsas': titulo_grafico_bolsas,

                'tabela_bolsas': tabela_bolsas,
                'titulo_tabela_bolsas': titulo_tabela_bolsas,

                'grafico_prod_docentes': grafico_prod,
                'titulo_prod_docentes': titulo_prod,

                'grafico_historico_prod': grafico_prod_historico,
                'titulo_historico_prod': titulo_prod_historico,

                'regulador': 'regulador',
                'numero_docentes': numero_docentes,

                'informacoes_card': programas_departamento,
                'dropdown_label':  dropdown_label,
                'card_2_titulo': 'Programas da Faculdade'
            }

            return render(request, 'home/departamentos.html', context)

        except:
            context = {}
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))


def sobre_nos(request):
    menu_nav_table = [
        {
            'titulo': 'Sobre nós',

            'text1': 'Sobre o projeto',

            'text2': 'Portal de dados',

            'text3': 'Escritório de apoio institucional ao pesquisador - EAIP | FFLCH'
        }
    ]
    context = {
        'landingpage' : True,
        'menu_table' : menu_nav_table
    }
    return render(request, 'home/sobre-nos.html', context)