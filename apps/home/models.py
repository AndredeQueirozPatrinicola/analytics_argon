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
    api_docente = models.JSONField()                                             # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                           # https://dados.fflch.usp.br/api/programas
    #api_programas_docente = models.JSONField()                                   # https://dados.fflch.usp.br/api/programas/docente/<id_docente>
    api_pesquisa = models.JSONField()                                            # https://dados.fflch.usp.br/api/pesquisa + 'filtro=departamento&ano_ini=&ano_fim=&serie_historica_tipo='


