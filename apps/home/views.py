from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

from services.populadb.Docentes import ApiDocente

from apps.home.models import Docente, Departamento

from .classes.docente import DadosDocente
from .classes.departamento import DadosDepartamento
from .classes.departamentos import Departamentos
from .classes.index import Index

class IndexView(View):

    def get(self, request):
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
        }

        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))


class DocenteView(View):

    def queries(self, numero_lattes):
        try:
            querie = Docente.objects.filter(docente_id=numero_lattes).values()
            querie = querie[0]

            api_docente = querie.get('api_docente')
            api_programas = querie.get('api_programas')
            api_docentes = querie.get('api_docentes')
        except:
            docente = ApiDocente(numero_lattes)
            api_programas = docente.pega_api_programas()
            api_docente = docente.pega_api_docente()
            api_docentes = docente.pega_api_docentes()

        return api_docente, api_programas, api_docentes

    def get(self, request, sigla, numero_lattes):
        docente = DadosDocente(numero_lattes, sigla)
        api_docente, api_programas, api_docentes = self.queries(numero_lattes)

        informacoes_docente = docente.pega_informacoes_basicas(api_programas, api_docentes)
        tabela_orientandos = docente.tabela_orientandos(api_docente)
        grafico_mestre_dout = docente.plota_grafico_orientandos(api_docente)
        grafico_artigos = docente.plota_grafico_historico('artigos', api_docente)
        grafico_livros = docente.plota_grafico_historico('livros', api_docente)
        grafico_capitulos = docente.plota_grafico_historico('capitulos', api_docente)
        tabela_publicacoes = docente.tabela_ultimas_publicacoes(api_docente)
        caminho = docente.pega_caminho(api_programas, api_docentes)
        linhas_pesquisa = docente.linhas_de_pesquisa(api_docente)
        tipo_vinculo_situacao = docente.pega_vinculo_situacao(api_docentes)

        """
            Dados dos cards que ficam no header da pagina.
            O header é o mesmo para todas as paginas, por isso a necessidade
            de alguns nomes genéricos como 'card_1', 'card_1_titulo'.
            Existem algumas variações que são tratadas diretamente no template do header.
        """ 
        context = {
            # Card 1
            'sigla_departamento': sigla,
            'docente': informacoes_docente, 
            'card_1_titulo': 'Nome / Lattes',
            # Card 2
            'informacoes_card': linhas_pesquisa.get('linhas_pesquisa'),
            'dropdown_label': linhas_pesquisa.get('label'),
            'card_2_titulo': 'Linhas de pesquisa', 
            # Card 3
            'card_3': tipo_vinculo_situacao.get('vinculo'), 
            'card_3_titulo': 'Tipo de vínculo',
            # Card 4
            'card_4': tipo_vinculo_situacao.get('situacao'),
            'card_4_titulo': 'Situação atual',
            # Caminho da navegação.
            'caminho': caminho,
            # Graficos e tabelas
            'tabela_orientandos': tabela_orientandos,
            'grafico_orientandos': grafico_mestre_dout,
            'tabela_publicacoes': tabela_publicacoes,
            'grafico_artigos': grafico_artigos,
            'grafico_livros': grafico_livros,
            'grafico_capitulos': grafico_capitulos,
        }

        return render(request, 'home/docentes.html', context)


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

        queries = {
            'api_docentes' : api_docentes, 
            'api_programas' : api_programas,
            'api_programas_docente' : api_programas_docente,
            'api_pesquisa' : api_pesquisa,
            'api_pesquisa_parametros' : api_pesquisa_parametros,
            'api_programas_docente_limpo' : api_programas_docente_limpo,
            'api_defesas' : api_defesas
        }

        return queries
    
    def get(self, request, sigla):

        departamento = DadosDepartamento(sigla)

        queries = self.queries(sigla)

        tabela_docentes = departamento.tabela_docentes(queries.get('api_programas'), queries.get('api_docentes'))
        numero_docentes = departamento.pega_numero_docentes(queries.get('api_programas'), queries.get('api_docentes'))
        grafico_pizza_aposentados_ativos = departamento.plota_aposentados_ativos(queries.get('api_programas'), queries.get('api_docentes'))
        grafico_pizza_tipo_vinculo = departamento.plota_tipo_vinculo_docente(queries.get('api_docentes'))
        grafico_prod_docentes = departamento.plota_prod_departamento(queries.get('api_programas_docente_limpo'))
        grafico_historico_prod = departamento.plota_prod_serie_historica(queries.get('api_programas_docente'))
        grafico_bolsas = departamento.plota_grafico_bolsa_sem(queries.get('api_pesquisa_parametros'))
        tabela_bolsas = departamento.tabela_trabalhos(queries.get('api_pesquisa'))
        programas_dpto = departamento.pega_programa_departamento()
        tabela_defesas = departamento.pega_tabela_defesas(queries.get('api_defesas'))
        grafico_defesa_mestrado_doutorado = departamento.defesas_mestrado_doutorado(queries.get('api_defesas'))

        caminho = [
            {
                'text': tabela_docentes.get('nome'),
                'url': '/departamento/' + sigla
            }
        ]

        context = {
            # Informações gerais e fragmentadas
            'regulador': 'regulador',
            'caminho': caminho,
            'nome': tabela_docentes.get('nome'),
            'id_lattes': id,
            'docentes': departamento,
            'df': tabela_docentes.get('df'),
            'lattes_id': tabela_docentes.get('id_lattes'),
            'tabela': 'docentes',
            'sigla_departamento': sigla,
            'numero_docentes': numero_docentes,
            # Graficos e tabelas
            'grafico_defesa_mestrado_doutorado' : grafico_defesa_mestrado_doutorado,
            'tabela_defesas' : tabela_defesas,
            'grafico_aposentados_ativos': grafico_pizza_aposentados_ativos,
            'grafico_tipo_vinculo': grafico_pizza_tipo_vinculo,
            'grafico_prod_docentes': grafico_prod_docentes,
            'tabela_bolsas': tabela_bolsas,
            'grafico_bolsas': grafico_bolsas,
            'grafico_historico_prod': grafico_historico_prod,
            # Card 2 -> Programas
            'informacoes_card': programas_dpto.get('programas_dpto'),
            'dropdown_label': programas_dpto.get('label'),
            'card_2_titulo': 'Programas do departamento'

        }

        return render(request, 'home/departamento.html', context)




class DepartamentosView(View):

    def queries(self):
        numero_docentes = Docente.objects.count()
        api_docentes = Docente.objects.values('api_docentes')

    def get(self, request):
        departamentos = Departamentos()
        try:
            tabela_todos_docentes = departamentos.tabela_todos_docentes()
            grafico_relacao_cursos = departamentos.plota_relacao_cursos()
            grafico_bolsas = departamentos.grafico_bolsa_sem()
            tabela_bolsas = departamentos.tabela_bolsas()
            grafico_producao_total_departamento = departamentos.prod_total_departamentos()
            grafico_historico_prod = departamentos.prod_historica_total()
            numero_docentes = departamentos.pega_numero_docentes()
            programas_departamento = departamentos.pega_programas()

            caminho = [
                {
                    'text': 'Departamentos',
                }
            ]

            context = {
                'regulador': 'regulador',
                'caminho': caminho,

                'df_docentes': tabela_todos_docentes.get('df'),
                'titulo_tabela_todos_docentes': tabela_todos_docentes.get('titulo'),

                'grafico_relacao_cursos':  grafico_relacao_cursos,
                'grafico_bolsas': grafico_bolsas,
                'tabela_bolsas': tabela_bolsas,
                'grafico_prod_docentes': grafico_producao_total_departamento,
                'grafico_historico_prod': grafico_historico_prod,

                'numero_docentes': numero_docentes,

                'informacoes_card': programas_departamento.get('programas'),
                'dropdown_label':  programas_departamento.get('label'),
                'card_2_titulo': 'Programas da Faculdade'
            }

            return render(request, 'home/departamentos.html', context)
        except:
            context = {}
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))

class SobrenosView(View):

    def get(self, request):
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