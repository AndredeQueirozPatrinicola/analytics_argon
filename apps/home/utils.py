
class Utils:

    def __init__(self):
        self.dptos_programas = {
            'FLP': [8131],
            'FSL': [8132],
            'FLF': [8133],
            'FLA': [8134],
            'FLG': [8135, 8136],
            'FLH': [8137, 8138],
            'FLL': [8139],
            'FLC': [8142, 8143, 8149, 8150, 8156, 8162],
            'FLM': [8144, 8145, 8146, 8147, 8148, 8158, 8160, 8163, 8164, 8165],
            'FLT': [8151],
            'FLO': [8155, 8157],
        }
        self.codigo_programas = {
                8131: 'Ciência Política',
                8132: 'Sociologia',
                8133: 'Filosofia',
                8134: 'Antropologia Social',
                8135: 'Geografia Física',
                8136: 'Geografia Humana',
                8137: 'História Econômica',
                8138: 'História Social',
                8139: 'Semiótica e Linguística Geral',
                8142: 'Filologia e Língua Portuguesa',
                8143: 'Letras Clássicas',
                8149: 'Literatura Brasileira',
                8150: 'Literatura Portuguesa',
                8156: 'Estudos Comparados de Literaturas de Língua Portuguesa',
                8162: 'Mestrado Profissional em Letras em Rede Nacional',
                8144: 'Língua e Literatura Alemã',
                8145: 'Língua Espanhola e Literaturas Espanhola e Hispano-Americana',
                8146: 'Estudos Lingüísticos, Literários e Tradutológicos em Francês',
                8147: 'Estudos Lingüísticos e Literários em Inglês',
                8148: 'Língua, Literatura e Cultura Italianas',
                8158: 'Estudos Judaicos',
                8160: 'Estudos da Tradução',
                8163: 'Estudos Linguísticos',
                8164: 'Estudos Literários e Culturais',
                8165: 'Estudos da Tradução',
                8151: 'Teoria Literária e Literatura Comparada',
                8155: 'Literatura e Cultura Russa',
                8157: 'Língua, Literatura e Cultura Japonesa'

            }

        self.dptos_siglas = {
                'FLA': 'Antropologia',
                'FLP': 'Ciência Política',
                'FLF': 'Filosofia',
                'FLH': 'História',
                'FLC': "Letras Clássicas e Vernáculas",
                'FLM': "Letras Modernas",
                'FLO': 'Letras Orientais',
                'FLL': 'Lingüística',
                'FSL': 'Sociologia',
                'FLT': "Teoria Literária e Literatura Comparada",
                'FLG': 'Geografia'
            }
            
        self.codigos = [
                8131, 8132, 8133, 8134,
                8135, 8136, 8137, 8138,
                8139, 8142, 8143, 8149,
                8150, 8156, 8162, 8144,
                8145, 8146, 8147, 8148,
                8158, 8160, 8163, 8164,
                8165, 8151, 8155, 8157
            ]

    def pega_programas_departamento(self, *departamento):
        try:
            if len(departamento) > 1:
                raise Exception("Não é possivel passar mais de 1 parametro")


            if departamento != tuple():
                programas_siglas = self.dptos_programas.get(departamento[0])

                departamento_nome = self.dptos_siglas.get(departamento[0])

                resultado = [self.codigo_programas.get(
                    i) for i in self.codigo_programas if i in programas_siglas]

                resultado = {
                    'sigla': departamento,
                    'nome': departamento_nome,
                    'programas': resultado
                }
            else:
                resultado = {
                    'programas': [self.codigo_programas.get(i) for i in self.codigos]
                }

            return resultado
        except:
            return 'Houve um erro para encontrar os dados do departamento'

    def pega_departamento_programa(self, *programa):

        if programa:
            if len(programa) == 1:

                if type(programa[0]) == int:
                    depart = [i for i in self.dptos_programas if programa[0]
                              in self.dptos_programas.get(i)]
                    depart_nome = self.dptos_siglas.get(depart[0])

                if type(programa[0]) == str:
                    verifica = [
                        i for i in self.codigo_programas if self.codigo_programas.get(i) == programa[0]]
                    depart = [i for i in self.dptos_programas if verifica[0]
                              in self.dptos_programas.get(i)]
                    depart_nome = self.dptos_siglas.get(depart[0])

                resultado = {
                    'sigla': depart[0],
                    'nome': depart_nome
                }

                return resultado

            elif len(programa) > 1:
                raise Exception(
                    "A função aceita somente 1 parametro. parametro:int ou parametro:str")
        else:
            return self.dptos_siglas

    def pega_codigo_estado(self, *estado):

        estados = {
            'AC': 12,
            'AL': 27,
            'AM': 13,
            'AP': 16,
            'BA': 29,
            'CE': 23,
            'DF': 53,
            'ES': 32,
            'GO': 52,
            'MA': 21,
            'MG': 31,
            'MT': 51,
            'MS': 50,
            'PA': 15,
            'PB': 25,
            'PE': 26,
            'PI': 22,
            'PR': 41,
            'RJ': 33,
            'RN': 24,
            'RO': 11,
            'RR': 14,
            'RS': 43,
            'SC': 42,
            'SE': 28,
            'SP': 35,
            'TO': 17,
        }

        if not estado:
            return estados

        elif estado:
            return [estados.get(i) for i in estados if i in estado]


    def siglas_departamentos(self, siglas_departamentos):

        if siglas_departamentos == 'siglas':
            return ['FLA', 'FLP', 'FLF', 'FLH', 'FLC', 'FLM', 'FLO', 'FLL', 'FSL', 'FLT', 'FLG']

        elif siglas_departamentos == 'departamentos':
            return self.dptos_siglas
        else:
            raise Exception(
                "A função só aceita os parametros 'siglas' e 'departamentos'.")
