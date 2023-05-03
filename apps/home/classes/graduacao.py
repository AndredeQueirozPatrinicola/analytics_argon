import pandas as pd
import numpy as np
from datetime import datetime

from django.db import connections
from django.db.models import Q, Count

from apps.home.models import *
from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils
from .etl import Etl

class Graduacao:

    def __init__(self, graduacao=False) -> None:
        self.graduacao = graduacao
        self.cursor = connections['etl'].cursor()
        self.etl = Etl()
        
    def pega_caminho(self):
        return [
            {
                'text' : 'Graduação',
                'url' : '#'
            }
        ]

    def pega_numero_alunos_ativos(self):
        dados = Graduacoes.objects.using('etl').filter(situacao_curso = 'ativo')
        resultado = {
            'title' : 'Numero de Alunos Ativos',
            'text' : f"Alunos: {len(dados)}"
        }
        return resultado
    
    def pega_formandos_ano_passado(self):
        ano_passado = datetime.now().year - 1
        dados = Graduacoes.objects.using('etl').filter(tipo_encerramento_bacharel = "Conclusão", data_fim_vinculo__year = ano_passado).count()
        return {
            "title" : f"Numero de alunos formados em {ano_passado}",
            "text" : f"Formados: {dados}"
        }

    def pega_ingressantes_ano_vigente(self):
        ano_atual = datetime.now().year
        dados = Graduacoes.objects.using('etl').filter(data_inicio_vinculo__year = ano_atual).count()
        return {
            "title" : f"Numero de alunos ingressantes em {ano_atual}",
            "text" : f"Ingressantes: {dados}"
        }
    
    def pega_egressos_ano_vigente(self):
        ano_atual = datetime.now().year
        dados = Graduacoes.objects.using('etl').filter(~Q(tipo_encerramento_bacharel = "Conclusão"), data_fim_vinculo__year = ano_atual).count()
        return {
            "title" : f"Numero de concluintes em {ano_atual}",
            "text" : f"Egressos: {dados}"
        }

    def tabela_alunos(self):
        columns = ['Encerrado', 'Ativo', 'Trancado', 'Reativado', 'Suspenso']
        dados = Graduacoes.objects.using("etl").values("situacao_curso", "nome_curso").annotate(dcount=Count('*'))
        df = pd.DataFrame(dados)
        df_pivot = pd.pivot_table(df, index='nome_curso', columns='situacao_curso', values='dcount', aggfunc='sum', fill_value=0)
        df_pivot = df_pivot[columns]
        df_pivot = df_pivot.reset_index()
        
        tabela = {
            "columns" : ["Nome", *columns],
            "values" : df_pivot.values.tolist()
        }

        return tabela


