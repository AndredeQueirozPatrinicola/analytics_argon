import pandas as pd
import numpy as np
from datetime import datetime

from django.db import connections
from django.db.models import Q, Count

from apps.home.models import *
from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils
from .etl import Etl



class PosGraduacao:

    ano_atual = datetime.now().year

    def alunos_ativos(self):
        data = Posgraduacoes.objects.using('etl').filter(tipo_ultima_ocorrencia__in=["ACO", "MAR"]).aggregate(total=Count('*'))
        return {
            "title" : "Numero de alunos ativos",
            "text" : data.get('total')
        }
    
    def alunos_ingressantes(self):
        data = Posgraduacoes.objects.using('etl').filter(primeira_matricula__year=str(self.ano_atual)).aggregate(total=Count('*'))
        return {
            "title" : f"Numero de alunos ingressantes em {self.ano_atual}",
            "text" : data.get('total')
        }
    
    def alunos_concluintes(self):
        data = Posgraduacoes.objects.using('etl').filter(data_aprovacao_trabalho__year=str(self.ano_atual)).aggregate(total=Count('*'))
        return {
            "title" : f"Numero de alunos concluintes em {self.ano_atual}",
            "text" : data.get('total')
        }
    
    def desligados(self):
        data = Posgraduacoes.objects.using('etl').filter(data_ultima_ocorrencia__year=str(self.ano_atual), tipo_ultima_ocorrencia = "DES").aggregate(total=Count('*'))
        return {
            "title": f"Numero de alunos desligados em {self.ano_atual}",
            "text" : data.get('total')
        }
    
    def nome_areas(self):
        data = Posgraduacoes.objects.using('etl').filter(tipo_ultima_ocorrencia__in=["ACO", "MAR"]).values('nome_area').annotate(count=Count('*')).order_by('nome_area')
        programas = [i.get("nome_area") for i in data if i.get('nome_area')] 
        programas.insert(0, "Geral")
        return programas