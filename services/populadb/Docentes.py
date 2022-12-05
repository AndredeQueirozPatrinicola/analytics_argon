import requests
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.models import Docente

class ApiDocente:

    def __init__(self, numero_lattes: str):
        self.numero_lattes = numero_lattes

    def pega_api_docentes(self):
        res = requests.get('https://dados.fflch.usp.br/api/docentes')
        dados = res.json()

        for i in dados: 
                if i.get('id_lattes') == self.numero_lattes:
                    dados_api_docentes = i

        return dados_api_docentes

    def pega_api_programas(self):
        res = requests.get('https://dados.fflch.usp.br/api/programas')
        dados = res.json()

        dados_departamentos = dados['departamentos']
        dados_programas = dados['programas']

        x = 0
        dados_api_programas = []
        while x < len(dados_departamentos):
            if self.numero_lattes in dados_departamentos[x].get('id_lattes_docentes'):
                dados_api_programas.append(dados_departamentos[x])

            x += 1

        if dados_api_programas == []:
            dados_api_programas.append(dados_programas) 
        
        return dados_api_programas

    def pega_api_docente(self):
        res = requests.get('https://dados.fflch.usp.br/api/programas/docente/' + self.numero_lattes)
        dados = res.json()
        return dados


    def atualiza_ou_cria_docente(self, api_docente, api_programas, api_docentes):
        docente = Docente.objects.filter(docente_id = self.numero_lattes)
        
        if docente.exists():
        
            docente.update(
                            api_docente=api_docente,
                            api_programas=api_programas,
                            api_docentes=api_docentes
                          )
        else:

            docente = Docente(
                                docente_id=self.numero_lattes,
                                api_docente = api_docente,
                                api_programas = api_programas,
                                api_docentes = api_docentes
                              )

            docente.save()
