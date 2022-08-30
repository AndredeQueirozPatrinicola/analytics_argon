# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Docente(models.Model):
    docente_id = models.CharField(max_length=255)
    api_docente = models.JSONField()                                            # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                          # https://dados.fflch.usp.br/api/programas

 
class Departamento(models.Model):
    sigla = models.CharField(max_length=10)
    api_docentes = models.JSONField()                                             # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                           # https://dados.fflch.usp.br/api/programas
    api_programas_docente = models.JSONField()
    api_pesquisa = models.JSONField()  
    api_pesquisa_parametros = models.JSONField()                                          # https://dados.fflch.usp.br/api/pesquisa + 'filtro=departamento&ano_ini=&ano_fim=&serie_historica_tipo='
    api_programas_docente_limpo = models.JSONField(null=True)

