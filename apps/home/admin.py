# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.

from .models import Docente, Departamento

# Register your models here.



class DocenteAdmin(admin.ModelAdmin):
    list_display = ('docente_id','api_docente', 'api_programas' )


admin.site.register(Docente, DocenteAdmin)


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('sigla','api_docentes', 'api_programas', 'api_programas_docente', 'api_pesquisa', 'api_pesquisa_parametros', 'api_programas_docente_limpo' )


admin.site.register(Departamento, DepartamentoAdmin)