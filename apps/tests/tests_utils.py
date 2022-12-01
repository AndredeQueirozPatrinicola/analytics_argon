from django.test import TestCase

from apps.home.utils import Utils


class UtilsPegaProgramasDepartamentoTestCase(TestCase):

    def setUp(self):
        self.utils_teste = Utils()
        self.valores ={
            'programas': 
                    [
                        'Ciência Política', 'Sociologia', 'Filosofia', 'Antropologia Social', 
                        'Geografia Física', 'Geografia Humana', 'História Econômica', 'História Social', 
                        'Semiótica e Linguística Geral', 'Filologia e Língua Portuguesa', 'Letras Clássicas', 
                        'Literatura Brasileira', 'Literatura Portuguesa', 'Estudos Comparados de Literaturas de Língua Portuguesa', 
                        'Mestrado Profissional em Letras em Rede Nacional', 'Língua e Literatura Alemã', 
                        'Língua Espanhola e Literaturas Espanhola e Hispano-Americana', 'Estudos Lingüísticos, Literários e Tradutológicos em Francês', 
                        'Estudos Lingüísticos e Literários em Inglês', 'Língua, Literatura e Cultura Italianas', 'Estudos Judaicos', 'Estudos da Tradução', 
                        'Humanidades, Direitos e Outras Legitimidades', 'Estudos Linguísticos', 'Estudos Literários e Culturais', 'Estudos da Tradução', 
                        'Teoria Literária e Literatura Comparada', 'Literatura e Cultura Russa', 'Língua, Literatura e Cultura Japonesa', 'Estudos Árabes'
                    ]}

        self.departamentos = ['FLA', 'FLP', 'FLH', 'FLF',
                              'FLC', "FLM", "FLO", "FLL", 
                              "FSL", "FLT", "FLG", ]
        self.programas = [{
                                'sigla': ('FLA',),
                                'nome': 'Antropologia',
                                'programas': ['Antropologia Social']
                          },{
                                'sigla': ('FLP',),
                                'nome': 'Ciência Política', 
                                'programas': ['Ciência Política']
                            },{
                                'sigla': ('FLH',), 
                                'nome': 'História', 
                                'programas': [
                                                'História Econômica', 
                                                'História Social',
                                                'Humanidades, Direitos e Outras Legitimidades'
                                            ]
                            },{
                                'sigla': ('FLF',), 
                                'nome': 'Filosofia', 
                                'programas': ['Filosofia']
                            },{
                                'sigla': ('FLC',), 
                                'nome': 'Letras Clássicas e Vernáculas', 
                                'programas': [
                                                'Filologia e Língua Portuguesa', 
                                                'Letras Clássicas', 
                                                'Literatura Brasileira', 
                                                'Literatura Portuguesa', 
                                                'Estudos Comparados de Literaturas de Língua Portuguesa', 
                                                'Mestrado Profissional em Letras em Rede Nacional'
                                            ]
                            },{
                                'sigla': ('FLM',), 
                                'nome': 'Letras Modernas', 
                                'programas': [
                                                'Língua e Literatura Alemã',   
                                                'Língua Espanhola e Literaturas Espanhola e Hispano-Americana',
                                                'Estudos Lingüísticos, Literários e Tradutológicos em Francês', 
                                                'Estudos Lingüísticos e Literários em Inglês', 
                                                'Língua, Literatura e Cultura Italianas', 
                                                'Estudos Judaicos', 
                                                'Estudos da Tradução', 
                                                'Estudos Linguísticos', 
                                                'Estudos Literários e Culturais', 
                                                'Estudos da Tradução'
                                            ]
                            },{
                                'sigla': ('FLO',), 
                                'nome': 'Letras Orientais', 
                                'programas': [
                                                'Literatura e Cultura Russa', 
                                                'Língua, Literatura e Cultura Japonesa',
                                                'Estudos Árabes',
                                              ]
                            },{
                                'sigla': ('FLL',), 
                                'nome': 'Lingüística', 
                                'programas': 
                                            [
                                                'Semiótica e Linguística Geral'
                                            ]
                              },{
                                'sigla': ('FSL',), 
                                'nome': 'Sociologia', 
                                'programas': ['Sociologia']
                              },{
                                'sigla': ('FLT',), 
                                'nome': 'Teoria Literária e Literatura Comparada', 
                                'programas': ['Teoria Literária e Literatura Comparada']
                              },{
                                'sigla': ('FLG',), 
                                'nome': 'Geografia', 
                                'programas': [
                                                'Geografia Física', 
                                                'Geografia Humana'
                                              ]
                                }
                            ]

    def test_retorno_vazio(self):
        self.assertEquals(
            self.utils_teste.pega_programas_departamento(), self.valores)

    def test_retorna_com_parametro(self):
        x = 0
        for i in self.departamentos:
            self.assertEquals(self.utils_teste.pega_programas_departamento(
                self.departamentos[x]), self.programas[x])
            x += 1

    def test_erros(self):
        ERRO = 'Houve um erro para encontrar os dados do departamento'
        self.assertEquals(self.utils_teste.pega_programas_departamento(
            [i for i in range(100)]), ERRO)
        self.assertEquals(self.utils_teste.pega_programas_departamento(
            "ysaguysdagdygsuydgsdgausd"), ERRO)
        self.assertEquals(
            self.utils_teste.pega_programas_departamento(12312312321), ERRO)
        self.assertEquals(
            self.utils_teste.pega_programas_departamento({}), ERRO)
        self.assertEquals(
            self.utils_teste.pega_programas_departamento("FLA", "FLG"), ERRO)


class UtilsPegaDepartamentoPrograma(TestCase):

    def setUp(self):
        self.utils_teste = Utils()
        self.codigo_programas = [8131, 8132, 8133, 8134, 8135, 8136, 8137, 8138, 8139, 8142, 8143, 8149,
                                 8150, 8156, 8162, 8144, 8145, 8146, 8147, 8148, 8158, 8160, 8163, 8164, 8165, 8151, 8155, 8157]
        self.responses = [{'sigla': 'FLP', 'nome': 'Ciência Política'}, {'sigla': 'FSL', 'nome': 'Sociologia'}, {'sigla': 'FLF', 'nome': 'Filosofia'}, {'sigla': 'FLA', 'nome': 'Antropologia'}, {
        'sigla': 'FLG', 'nome': 'Geografia'}, {'sigla': 'FLG', 'nome': 'Geografia'}, {'sigla': 'FLH', 'nome': 'História'}, {'sigla': 'FLH', 'nome': 'História'}, {'sigla': 'FLL', 'nome': 'Lingüística'}, {'sigla': 'FLC', 'nome': 'Letras Clássicas e Vernáculas'}, {'sigla': 'FLC', 'nome': 'Letras Clássicas e Vernáculas'}, {'sigla': 'FLC', 'nome': 'Letras Clássicas e Vernáculas'}, {'sigla': 'FLC', 'nome': 'Letras Clássicas e Vernáculas'}, {'sigla': 'FLC', 'nome': 'Letras Clássicas e Vernáculas'}, {'sigla': 'FLC', 'nome': 'Letras Clássicas e Vernáculas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLM', 'nome': 'Letras Modernas'}, {'sigla': 'FLT', 'nome': 'Teoria Literária e Literatura Comparada'}, {'sigla': 'FLO', 'nome': 'Letras Orientais'}, {'sigla': 'FLO', 'nome': 'Letras Orientais'}]
        self.programas = ['Ciência Política','Sociologia','Filosofia','Antropologia Social','Geografia Física','Geografia Humana','História Econômica','História Social','Semiótica e Linguística Geral','Filologia e Língua Portuguesa','Letras Clássicas','Literatura Brasileira','Literatura Portuguesa','Estudos Comparados de Literaturas de Língua Portuguesa','Mestrado Profissional em Letras em Rede Nacional','Língua e Literatura Alemã','Língua Espanhola e Literaturas Espanhola e Hispano-Americana','Estudos Lingüísticos, Literários e Tradutológicos em Francês','Estudos Lingüísticos e Literários em Inglês','Língua, Literatura e Cultura Italianas','Estudos Judaicos','Estudos da Tradução','Estudos Linguísticos','Estudos Literários e Culturais','Estudos da Tradução','Teoria Literária e Literatura Comparada','Literatura e Cultura Russa','Língua, Literatura e Cultura Japonesa']


    def test_programa_codigo(self):
        x = 0
        for i in self.codigo_programas:
            self.assertEquals(self.utils_teste.pega_departamento_programa(self.codigo_programas[x]), self.responses[x])
            x += 1


    def test_programa_nome(self):
        x = 0
        for i in self.programas:
            self.assertEquals(self.utils_teste.pega_departamento_programa(self.programas[x]), self.responses[x])
            x += 1

       
    
class UtilsCodigoEstado(TestCase):

    def setUp(self):
        self.utils_teste = Utils()
        self.estados = {'AC' : 12,'AL' : 27,'AM' : 13,'AP' : 16,'BA' : 29,'CE' : 23,'DF' : 53,'ES' : 32,'GO' : 52,'MA' : 21,'MG' : 31,'MT' : 51,'MS' : 50,'PA' : 15,'PB' : 25,'PE' : 26,'PI' : 22,'PR' : 41,'RJ' : 33,'RN' : 24,'RO' : 11,'RR' : 14,'RS' : 43,'SC' : 42,'SE' : 28,'SP' : 35,'TO' : 17}
    
    def test_estados_vazio(self):
        self.assertEquals(self.utils_teste.pega_codigo_estado(), self.estados)

    def test_estados(self):
        x = 0
        for i in self.estados:
            self.assertEquals(self.utils_teste.pega_codigo_estado(list(self.estados)[x]), [self.estados.get(list(self.estados)[x])])
            x += 1

    def test_erro(self):
        ERRO = []
        self.assertEquals(self.utils_teste.pega_codigo_estado(
            [i for i in range(100)]), ERRO)
        self.assertEquals(self.utils_teste.pega_codigo_estado(
            "ysaguysdagdygsuydgsdgausd"), ERRO)
        self.assertEquals(
            self.utils_teste.pega_codigo_estado(12312312321), ERRO)
        self.assertEquals(
            self.utils_teste.pega_codigo_estado({}), ERRO)
        self.assertEquals(
            self.utils_teste.pega_codigo_estado("FLA", "FLG"), ERRO)

