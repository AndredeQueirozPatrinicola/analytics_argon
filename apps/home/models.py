from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Docente(models.Model):
    docente_id = models.CharField(max_length=255)
    api_docente = models.JSONField()                                            # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                          # https://dados.fflch.usp.br/api/programas
    api_docentes = models.JSONField(null=True)                                  # https://dados.fflch.usp.br/api/docentes

    def __str__(self):
        return self.docente_id
 
 
class Departamento(models.Model):
    sigla = models.CharField(max_length=10)
    api_docentes = models.JSONField()                                             # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                           # https://dados.fflch.usp.br/api/programas
    api_programas_docente = models.JSONField()
    api_pesquisa = models.JSONField()  
    api_pesquisa_parametros = models.JSONField()                                # https://dados.fflch.usp.br/api/pesquisa + 'filtro=departamento&ano_ini=&ano_fim=&serie_historica_tipo='
    api_programas_docente_limpo = models.JSONField(null=True)
    api_defesas = models.JSONField(null=True)

    def __str__(self):
        return self.sigla


class Mapa(models.Model):
    nome = models.CharField(max_length=255)
    base_de_dados = models.JSONField(null=True)
    dados_do_mapa = models.JSONField(null=True)

    def __str__(self) -> str:
        return self.nome


class AlunosGraduacao(models.Model):
    numeroUSP_id = models.IntegerField(primary_key=True, db_column='numeroUSP')
    nomeAluno = models.CharField(max_length=256)
    anoNascimento = models.IntegerField()
    email = models.CharField(max_length=128)
    nacionalidade = models.CharField(max_length=128)
    cidadeNascimento = models.CharField(max_length=128)
    estadoNascimento = models.CharField(max_length=2)
    paisNascimento = models.CharField(max_length=128)
    raca = models.CharField(max_length=32)
    sexo = models.CharField(max_length=1)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'alunos_graduacao'

class Graduacoes(models.Model):
    idGraduacao = models.CharField(max_length=32, primary_key=True)
    numeroUSP_id = models.ForeignKey(AlunosGraduacao, on_delete=models.CASCADE, db_column='numeroUSP')
    sequenciaCurso = models.SmallIntegerField()
    situacao = models.CharField(max_length=16)
    dataInicioVinculo = models.DateTimeField()
    dataFimVinculo = models.DateTimeField()
    codigoCurso = models.IntegerField()
    nomeCurso = models.CharField(max_length=32)
    tipoIngresso = models.CharField(max_length=64)
    categoriaIngresso = models.CharField(max_length=64)
    rankIngresso = models.SmallIntegerField()
    tipoEncerramento = models.CharField(max_length=128)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'graduacoes'