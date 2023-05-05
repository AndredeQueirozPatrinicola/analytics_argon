from datetime import datetime

from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.shortcuts import  render

from services.populadb.Docentes import ApiDocente

from apps.home.models import Docente, Departamento

from .classes.docente import DadosDocente
from .classes.departamento import DadosDepartamento
from .classes.departamentos import Departamentos
from .classes.index import Index
from .classes.graduacao import Graduacao
from .utils import Utils


class IndexView(View):

    def get(self, request):
        index = Index()
        try:
            globo = index.plota_mapa()
        except:
            globo = None

        menu_nav_table, titulo_menu = index.tabela_sobrenos()
        tabela_mapa = index.tabela_alunos_estados()


        context = {
            'segment': 'index',
            'landingpage': 'landingpage',

            'titulo': titulo_menu,
            'menu_table': menu_nav_table,

            'globo': globo,
            'tabela_mapa' : tabela_mapa,
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

        queries = {
            'api_docente' : api_docente,
            'api_programas' : api_programas,
            'api_docentes' : api_docentes
        }

        return queries

    def get(self, request, *args, **kwargs):
        
        if numerolattes:=self.kwargs.get('docente'):
            docente = DadosDocente(numerolattes)
            queries = self.queries(numerolattes)

            api_docente = queries.get('api_docente')
            api_programas = queries.get('api_programas')  
            api_docentes = queries.get('api_docentes')

            caminho = docente.pega_caminho(api_programas, api_docentes)
            cards = docente.pega_informacoes_basicas(api_programas, api_docente, api_docentes, novo="novo")
            tabela_orientandos = docente.tabela_orientandos(api_docente)
            tabela_publicacoes = docente.tabela_ultimas_publicacoes(api_docente)

            context = {
                'caminho' : caminho,
                'card_header_1' :  cards.get('card_header_1'),
                'card_header_2' :  cards.get('card_header_2'),
                'card_header_3' :  cards.get('card_header_3'),
                'card_header_4' :  cards.get('card_header_4'),
                'tabela_orientandos' : tabela_orientandos,
                'tabela_publicacoes' : tabela_publicacoes
            } 
            return render(request, 'home/docente.html', context)
        else:
            return render(request, 'home/docentes.html')

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
        tabela_bolsas = departamento.tabela_trabalhos(queries.get('api_pesquisa'))
        programas_dpto = departamento.pega_programa_departamento()
        tabela_defesas = departamento.pega_tabela_defesas(queries.get('api_defesas'))

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
            'tabela_defesas' : tabela_defesas,
            'tabela_bolsas': tabela_bolsas,
            # Card 2 -> Programas
            'informacoes_card': programas_dpto.get('programas_dpto'),
            'dropdown_label': programas_dpto.get('label'),
            'card_2_titulo': 'Programas do departamento'

        }

        return render(request, 'home/departamento.html', context)




class DepartamentosView(View):

    def queries(self):
        querie_departamentos = Departamento.objects.values('api_pesquisa_parametros', 'api_programas_docente_limpo', 'api_programas_docente', 'api_defesas')
        querie_docentes = Docente.objects.values('api_docentes')

        queries = {
            'querie_departamentos' : querie_departamentos,
            'querie_docentes' : querie_docentes
        }

        return queries
        

    def get(self, request):
        queries = self.queries()
        querie_departamentos = queries.get('querie_departamentos')
        querie_docente = queries.get('querie_docentes')
        departamentos = Departamentos(querie_departamentos, querie_docente)

        numero_docentes = departamentos.pega_numero_docentes()
        tabela_todos_docentes = departamentos.tabela_todos_docentes()
        tabela_defesas = departamentos.tabela_defesas()

        caminho = [
            {
                'text': 'Departamentos',
            }
        ]

        utils = Utils()
        departamentos_ = ["Geral", *list(utils.siglas_dptos.keys())]
        context = {
            'departamentos' : departamentos_,
            'caminho' : caminho,

            'card_header_1' : {
                    'title' : numero_docentes.get('titulo'),
                    'text' : numero_docentes.get('texto_ativos').get('total')
            },
            'df_docentes' : tabela_todos_docentes,
            'df_defesas' : tabela_defesas
        }

        return render(request, 'home/departamentos.html', context)


class SobrenosView(View):

    def get(self, request):
        context = {
            'landingpage': 'landingpage'
        }
        return render(request, 'home/projeto.html', context)


class AbstractGraduacaoViews(View):
    graduacao = Graduacao()
    utils = Utils()

    def get(self, request):
        
        departamentos = ["Geral", "Geografia" , "Historia", "Letras", "Ciências Sociais", "Filosofia"]
        departamentos_pos = list(self.utils.dptos_siglas.values())
        departamentos_pos.insert(0, "Geral")
        
        numero_alunos = self.graduacao.pega_numero_alunos_ativos()
        numero_formandos = self.graduacao.pega_formandos_ano_passado()
        numero_ingressantes = self.graduacao.pega_ingressantes_ano_vigente()
        numero_egressos = self.graduacao.pega_egressos_ano_vigente()

        anos = [ano for ano in range(2013, datetime.now().year + 1)]
        anos_reverse = list(reversed(anos))

        context = { 
            "card_header_1": numero_alunos,
            "card_header_2" : numero_formandos,
            "card_header_3" : numero_ingressantes,
            "card_header_4" : numero_egressos,
            "departamentos" : departamentos,
            "departamentos_pos" : departamentos_pos,
            "anos" : anos,
            "anos_reverse": anos_reverse
        }
        return [request, 'home/graduacao.html', context]
    
class GraduacaoDiversidade(AbstractGraduacaoViews):

    def get(self, request):
        payload = super().get(request)
        payload[1] = 'home/graduacao_diversidade.html'

        context = payload[-1]
        caminho = [
            {
                'text' : 'Graduação',
                'url' : '/graduacao/geral'
            },
            {
                'text' : 'Diversidade',
                'url' : '#'
            }
        ]

        context['caminho'] = caminho

        return render(*payload)
    
class GraduacaoGeral(AbstractGraduacaoViews):

    def get(self, request):
        payload = super().get(request)
        payload[1] = 'home/graduacao_geral.html'

        context = payload[-1]
        caminho = [
            {
                'text' : 'Graduação',
                'url' : '/graduacao/geral'
            },
            {
                'text' : 'Geral',
                'url' : '#'
            }
        ]

        tabela_alunos = self.graduacao.tabela_alunos()
        context['caminho'] = caminho
        context["tabela_alunos"] = tabela_alunos
        return render(*payload)
    
class GraduacaoPesquisa(AbstractGraduacaoViews):

    def get(self, request):
        payload = super().get(request)
        payload[1] = 'home/graduacao_pesquisa.html'
        context = payload[-1]
        tabela_ics = self.graduacao.tabela_iniciacao()

        caminho = [
            {
                'text' : 'Graduação',
                'url' : '/graduacao/geral'
            },
            {
                'text' : 'Pesquisa',
                'url' : '#'
            }
        ]

        context['caminho'] = caminho
        context['tabela_ics'] = tabela_ics
        return render(*payload)
