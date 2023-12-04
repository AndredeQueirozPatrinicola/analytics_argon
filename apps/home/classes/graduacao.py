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
        dados = Graduacoes.objects.using('etl').filter(situacao_curso = 'ativo').count()
        resultado = {
            'title' : 'Numero de Alunos Ativos',
            #'text': dados
            'text' : f"Alunos: {dados}"
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
            "text" : f"Concluintes: {dados}"
        }

    def tabela_alunos(self):
        columns = ['Encerrado', 'Ativo', 'Trancado', 'Suspenso']
        dados = Graduacoes.objects.using("etl").values("situacao_curso", "nome_curso").annotate(dcount=Count('*'))
        df = pd.DataFrame(dados)
        df_pivot = pd.pivot_table(df, index='nome_curso', columns='situacao_curso', values='dcount', aggfunc='sum', fill_value=0)
        df_pivot = df_pivot[columns]
        df_pivot = df_pivot.reset_index()
        
        total = {
            'nome_curso': 'Total',
            'Encerrado': df_pivot['Encerrado'].sum(),
            'Ativo': df_pivot['Ativo'].sum(),
            'Trancado': df_pivot['Trancado'].sum(),
            'Suspenso': df_pivot['Suspenso'].sum()
        }
        df_pivot = df_pivot.append(total, ignore_index=True)

        tabela = {
            "columns" : ["Nome", *columns],
            "values" : df_pivot.values.tolist()
        }

        return tabela
    
    def tabela_iniciacao(self):
        columns = ["Agencias de fomento", "Departamentos", "Contagem"]
        data = self.etl.group_by(
                                columns=[
                                    "y.nome_fomento", 
                                    "x.nome_departamento",
                                    "COUNT(*)"
                                ],
                                tables=[
                                    "iniciacoes",
                                    "bolsas_ic"
                                ],
                                ids="id_projeto",
                                condition={
                                    "situacao_projeto": "Ativo"
                                },
                                group_by=[
                                    "y.nome_fomento", 
                                    "x.nome_departamento"
                                ]
                            )

        df = pd.DataFrame(data, columns=columns)
        df = df.pivot_table(index="Departamentos", columns="Agencias de fomento", values="Contagem", fill_value=0)
    
        tabela_valores = df.values.tolist()
        for i in tabela_valores:
            i.insert(0, df.index[tabela_valores.index(i)])

        tabela = {
            "columns" : ["Departamento", *[i for i in df]],
            "values" : tabela_valores
        }

        return tabela


