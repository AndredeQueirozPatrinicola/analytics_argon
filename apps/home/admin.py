# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.

from .models import Docente

# Register your models here.



class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('docente_id','api_docente', 'api_programas' )


admin.site.register(Docente, FornecedorAdmin)