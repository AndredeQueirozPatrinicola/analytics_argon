from django.db import models


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

# class AfastempresasPosdoc(models.Model):
#     id_projeto = models.OneToOneField('PeriodosPosdoc', models.DO_NOTHING, db_column='id_projeto', primary_key=True)
#     sequencia_periodo = models.ForeignKey('PeriodosPosdoc', models.DO_NOTHING, db_column='sequencia_periodo')
#     seq_vinculo_empresa = models.IntegerField()
#     nome_empresa = models.CharField(max_length=512)
#     data_inicio_afastamento = models.DateField(blank=True, null=True)
#     data_fim_afastamento = models.DateField(blank=True, null=True)
#     tipo_vinculo = models.CharField(max_length=64, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'afastempresas_posdoc'
#         unique_together = (('id_projeto', 'sequencia_periodo', 'seq_vinculo_empresa'),)


class AlunosGraduacao(models.Model):
    numerousp = models.IntegerField(db_column='numeroUSP', primary_key=True)  # Field name made lowercase.
    nomealuno = models.CharField(db_column='nomeAluno', max_length=256)  # Field name made lowercase.
    anonascimento = models.SmallIntegerField(db_column='anoNascimento')  # Field name made lowercase.
    email = models.CharField(max_length=128, blank=True, null=True)
    nacionalidade = models.CharField(max_length=128, blank=True, null=True)
    cidadenascimento = models.CharField(db_column='cidadeNascimento', max_length=128, blank=True, null=True)  # Field name made lowercase.
    estadonascimento = models.CharField(db_column='estadoNascimento', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisnascimento = models.CharField(db_column='paisNascimento', max_length=128, blank=True, null=True)  # Field name made lowercase.
    raca = models.CharField(max_length=32, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'alunos_graduacao'


class AlunosPosdoc(models.Model):
    numerousp = models.IntegerField(db_column='numeroUSP', primary_key=True)  # Field name made lowercase.
    nomealuno = models.CharField(db_column='nomeAluno', max_length=256)  # Field name made lowercase.
    anonascimento = models.SmallIntegerField(db_column='anoNascimento')  # Field name made lowercase.
    nacionalidade = models.CharField(max_length=128, blank=True, null=True)
    cidadenascimento = models.CharField(db_column='cidadeNascimento', max_length=128, blank=True, null=True)  # Field name made lowercase.
    estadonascimento = models.CharField(db_column='estadoNascimento', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisnascimento = models.CharField(db_column='paisNascimento', max_length=128, blank=True, null=True)  # Field name made lowercase.
    raca = models.CharField(max_length=32, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'alunos_posdoc'


class AlunosPosgraduacao(models.Model):
    numerousp = models.IntegerField(db_column='numeroUSP', primary_key=True)  # Field name made lowercase.
    nomealuno = models.CharField(db_column='nomeAluno', max_length=256)  # Field name made lowercase.
    anonascimento = models.SmallIntegerField(db_column='anoNascimento')  # Field name made lowercase.
    nacionalidade = models.CharField(max_length=128, blank=True, null=True)
    cidadenascimento = models.CharField(db_column='cidadeNascimento', max_length=128, blank=True, null=True)  # Field name made lowercase.
    estadonascimento = models.CharField(db_column='estadoNascimento', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisnascimento = models.CharField(db_column='paisNascimento', max_length=128, blank=True, null=True)  # Field name made lowercase.
    raca = models.CharField(max_length=32, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'alunos_posgraduacao'


class BolsasIc(models.Model):
    id_projeto = models.ForeignKey('Iniciacoes', models.DO_NOTHING, db_column='id_projeto')
    sequencia_bolsa = models.IntegerField()
    nome_programa = models.CharField(max_length=128)
    bolsa_edital = models.IntegerField(blank=True, null=True)
    data_inicio_bolsa = models.DateField(blank=True, null=True)
    data_fim_bolsa = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bolsas_ic'


# class BolsasPosdoc(models.Model):
#     id_projeto = models.OneToOneField('PeriodosPosdoc', models.DO_NOTHING, db_column='id_projeto', primary_key=True)
#     sequencia_periodo = models.ForeignKey('PeriodosPosdoc', models.DO_NOTHING, db_column='sequencia_periodo')
#     sequencia_fomento = models.IntegerField()
#     codigo_fomento = models.SmallIntegerField(blank=True, null=True)
#     nome_fomento = models.CharField(max_length=256, blank=True, null=True)
#     data_inicio_fomento = models.DateField(blank=True, null=True)
#     data_fim_fomento = models.DateField(blank=True, null=True)
#     id_fomento = models.CharField(max_length=64, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'bolsas_posdoc'
#         unique_together = (('id_projeto', 'sequencia_periodo', 'sequencia_fomento'),)


class CursosCulturaextensao(models.Model):
    codigo_curso_ceu = models.IntegerField(primary_key=True)
    sigla_unidade = models.CharField(max_length=16)
    codigo_departamento = models.IntegerField(blank=True, null=True)
    nome_departamento = models.CharField(max_length=64, blank=True, null=True)
    modalidade_curso = models.CharField(max_length=32)
    nome_curso = models.CharField(max_length=256)
    tipo = models.CharField(max_length=32)
    codigo_colegiado = models.SmallIntegerField()
    sigla_colegiado = models.CharField(max_length=32)
    area_conhecimento = models.CharField(max_length=128)
    area_tematica = models.CharField(max_length=128)
    linha_extensao = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'cursos_culturaextensao'


class Graduacoes(models.Model):
    id_graduacao = models.CharField(primary_key=True, max_length=32)
    numero_usp = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='numero_usp')
    sequencia_grad = models.IntegerField()
    situacao_curso = models.CharField(max_length=16)
    data_inicio_vinculo = models.DateField()
    data_fim_vinculo = models.DateField(blank=True, null=True)
    codigo_curso = models.IntegerField()
    nome_curso = models.CharField(max_length=32)
    tipo_ingresso = models.CharField(max_length=64)
    categoria_ingresso = models.CharField(max_length=64, blank=True, null=True)
    rank_ingresso = models.SmallIntegerField(blank=True, null=True)
    tipo_encerramento_bacharel = models.CharField(max_length=128, blank=True, null=True)
    data_encerramento_bacharel = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'graduacoes'


class Habilitacoes(models.Model):
    id_graduacao = models.ForeignKey(Graduacoes, models.DO_NOTHING, db_column='id_graduacao')
    codigo_curso = models.IntegerField()
    codigo_habilitacao = models.IntegerField()
    nome_habilitacao = models.CharField(max_length=64)
    tipo_habilitacao = models.CharField(max_length=32)
    periodo_habilitacao = models.CharField(max_length=32)
    data_inicio_habilitacao = models.DateField()
    data_fim_habilitacao = models.DateField(blank=True, null=True)
    tipo_encerramento = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habilitacoes'


class Iniciacoes(models.Model):
    id_projeto = models.CharField(primary_key=True, max_length=12)
    numero_usp = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='numero_usp')
    status_projeto = models.CharField(max_length=32)
    ano_projeto = models.SmallIntegerField()
    codigo_departamento = models.IntegerField()
    nome_departamento = models.CharField(max_length=64)
    data_inicio_projeto = models.DateField(blank=True, null=True)
    data_fim_projeto = models.DateField(blank=True, null=True)
    numero_usp_orientador = models.IntegerField(blank=True, null=True)
    titulo_projeto = models.CharField(max_length=256)
    palavras_chave = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'iniciacoes'


class InscricoesCcex(models.Model):
    codigo_oferecimento = models.ForeignKey('OferecimentosCcex', models.DO_NOTHING, db_column='codigo_oferecimento')
    numero_ceu = models.IntegerField(blank=True, null=True)
    data_inscricao = models.DateTimeField(blank=True, null=True)
    situacao_inscricao = models.CharField(max_length=32, blank=True, null=True)
    origem_inscricao = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inscricoes_ccex'


class MatriculasCcex(models.Model):
    codigo_matricula_ceu = models.IntegerField(primary_key=True)
    numero_usp = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='numero_usp')
    codigo_oferecimento = models.ForeignKey('OferecimentosCcex', models.DO_NOTHING, db_column='codigo_oferecimento')
    data_matricula = models.DateTimeField()
    status_matricula = models.CharField(max_length=16)
    data_inicio_curso = models.DateField()
    data_fim_curso = models.DateField()
    frequencia_aluno = models.IntegerField(blank=True, null=True)
    conceito_final_aluno = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matriculas_ccex'


class OferecimentosCcex(models.Model):
    codigo_oferecimento = models.CharField(primary_key=True, max_length=32)
    codigo_curso_ceu = models.ForeignKey(CursosCulturaextensao, models.DO_NOTHING, db_column='codigo_curso_ceu')
    situacao_oferecimento = models.CharField(max_length=32, blank=True, null=True)
    data_inicio_oferecimento = models.DateField()
    data_fim_oferecimento = models.DateField()
    total_carga_horaria = models.SmallIntegerField(blank=True, null=True)
    qntd_vagas_ofertadas = models.SmallIntegerField()
    curso_pago = models.CharField(max_length=1)
    valor_inscricao_edicao = models.SmallIntegerField(blank=True, null=True)
    qntd_vagas_gratuitas = models.SmallIntegerField(blank=True, null=True)
    valor_previsto_arrecadacao = models.IntegerField(blank=True, null=True)
    valor_previsto_custos = models.SmallIntegerField(blank=True, null=True)
    valor_previsto_prce = models.SmallIntegerField(blank=True, null=True)
    curso_para_empresas = models.CharField(max_length=1)
    local_curso = models.CharField(max_length=256)
    data_inicio_inscricoes = models.DateField()
    data_fim_inscricoes = models.DateField()
    permite_inscricao_online = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oferecimentos_ccex'


class PeriodosPosdoc(models.Model):
    id_projeto = models.OneToOneField('ProjetosPosdoc', models.DO_NOTHING, db_column='id_projeto', primary_key=True)
    sequencia_periodo = models.SmallIntegerField()
    data_inicio_periodo = models.DateField()
    data_fim_periodo = models.DateField(blank=True, null=True)
    situacao_periodo = models.CharField(max_length=32)
    fonte_recurso = models.CharField(max_length=32)
    horas_semanais = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'periodos_posdoc'
        unique_together = (('id_projeto', 'sequencia_periodo'),)


class Pessoas(models.Model):
    numero_usp = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=256)
    data_nascimento = models.DateField()
    email = models.CharField(max_length=128, blank=True, null=True)
    nacionalidade = models.CharField(max_length=128, blank=True, null=True)
    cidade_nascimento = models.CharField(max_length=128, blank=True, null=True)
    estado_nascimento = models.CharField(max_length=2, blank=True, null=True)
    pais_nascimento = models.CharField(max_length=128, blank=True, null=True)
    raca = models.CharField(max_length=32, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    cpf = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoas'


class Posgraduacoes(models.Model):
    id_pos_graduacao = models.CharField(primary_key=True, max_length=32)
    numero_usp = models.ForeignKey(Pessoas, models.DO_NOTHING, db_column='numero_usp')
    seq_programa = models.IntegerField()
    nivel_programa = models.CharField(max_length=2)
    codigo_area = models.IntegerField()
    nome_area = models.CharField(max_length=64, blank=True, null=True)
    codigo_programa = models.IntegerField()
    nome_programa = models.CharField(max_length=128, blank=True, null=True)
    data_selecao = models.DateField()
    primeira_matricula = models.DateField(blank=True, null=True)
    tipo_ultima_ocorrencia = models.CharField(max_length=32, blank=True, null=True)
    data_ultima_ocorrencia = models.DateField(blank=True, null=True)
    data_deposito_trabalho = models.DateField(blank=True, null=True)
    data_aprovacao_trabalho = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posgraduacoes'


class ProjetosPosdoc(models.Model):
    id_projeto = models.CharField(primary_key=True, max_length=12)
    programa = models.CharField(max_length=2)
    numero_usp = models.ForeignKey(Pessoas, models.DO_NOTHING, db_column='numero_usp')
    data_inicio_projeto = models.DateField(blank=True, null=True)
    data_fim_projeto = models.DateField(blank=True, null=True)
    situacao_projeto = models.CharField(max_length=16)
    codigo_departamento = models.IntegerField(blank=True, null=True)
    nome_departamento = models.CharField(max_length=256, blank=True, null=True)
    titulo_projeto = models.CharField(max_length=1024)
    palavras_chave = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projetos_posdoc'


class QuestionarioQuestoes(models.Model):
    id_questao = models.CharField(primary_key=True, max_length=12)
    descricao_questao = models.CharField(max_length=512)
    codigo_alternativa = models.IntegerField()
    descricao_alternativa = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionario_questoes'
        unique_together = (('id_questao', 'codigo_alternativa'),)


# class QuestionarioRespostas(models.Model):
#     id_graduacao = models.ForeignKey(Graduacoes, models.DO_NOTHING, db_column='id_graduacao')
#     id_questao = models.ForeignKey(QuestionarioQuestoes, models.DO_NOTHING, db_column='id_questao')
#     alternativa_escolhida = models.ForeignKey(QuestionarioQuestoes, models.DO_NOTHING, db_column='alternativa_escolhida')

#     class Meta:
#         managed = False
#         db_table = 'questionario_respostas'


class Servidores(models.Model):
    numero_usp = models.IntegerField(primary_key=True)
    nome_aluno = models.CharField(max_length=256)
    ano_nascimento = models.SmallIntegerField()
    nacionalidade = models.CharField(max_length=128, blank=True, null=True)
    cidade_nascimento = models.CharField(max_length=128, blank=True, null=True)
    estado_nascimento = models.CharField(max_length=2, blank=True, null=True)
    pais_nascimento = models.CharField(max_length=128, blank=True, null=True)
    raca = models.CharField(max_length=32, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servidores'


class SiicuspParticipantes(models.Model):
    id_trabalho = models.ForeignKey('SiicuspTrabalhos', models.DO_NOTHING, db_column='id_trabalho')
    tipo_participante = models.CharField(max_length=32)
    numero_usp = models.IntegerField(blank=True, null=True)
    nome_participante = models.CharField(max_length=128, blank=True, null=True)
    codigo_unidade = models.SmallIntegerField(blank=True, null=True)
    sigla_unidade = models.CharField(max_length=24, blank=True, null=True)
    codigo_departamento = models.IntegerField(blank=True, null=True)
    nome_departamento = models.CharField(max_length=256, blank=True, null=True)
    participante_apresentador = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'siicusp_participantes'


class SiicuspTrabalhos(models.Model):
    id_trabalho = models.CharField(primary_key=True, max_length=12)
    titulo_trabalho = models.CharField(max_length=512)
    id_projeto_ic = models.CharField(max_length=12, blank=True, null=True)
    edicao_siicusp = models.SmallIntegerField()
    situacao_inscricao = models.CharField(max_length=24)
    situacao_apresentacao = models.CharField(max_length=24, blank=True, null=True)
    prox_etapa_recomendado = models.IntegerField(blank=True, null=True)
    prox_etapa_apresentado = models.IntegerField(blank=True, null=True)
    mencao_honrosa = models.IntegerField(blank=True, null=True)
    codigo_dpto_orientador = models.IntegerField(blank=True, null=True)
    nome_dpto_orientador = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'siicusp_trabalhos'


class SupervisoesPosdoc(models.Model):
    id_projeto = models.OneToOneField(ProjetosPosdoc, models.DO_NOTHING, db_column='id_projeto', primary_key=True)
    sequencia_supervisao = models.SmallIntegerField()
    numero_usp_supervisor = models.IntegerField()
    nome_supervisor = models.CharField(max_length=256)
    tipo_supervisao = models.CharField(max_length=40)
    data_inicio_supervisao = models.DateField()
    data_fim_supervisao = models.DateField()
    ultimo_supervisor_resp = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'supervisoes_posdoc'
        unique_together = (('id_projeto', 'sequencia_supervisao', 'tipo_supervisao'),)


class VinculosServidores(models.Model):
    numero_usp = models.ForeignKey(Pessoas, models.DO_NOTHING, db_column='numero_usp')
    numero_sequencia_vinculo = models.SmallIntegerField()
    tipo_vinculo = models.CharField(max_length=48)
    data_inicio_vinculo = models.DateField()
    data_fim_vinculo = models.DateField(blank=True, null=True)
    situacao_atual = models.CharField(max_length=24)
    cod_ultimo_setor = models.IntegerField(blank=True, null=True)
    nome_ultimo_setor = models.CharField(max_length=128, blank=True, null=True)
    tipo_ingresso = models.CharField(max_length=128, blank=True, null=True)
    ultima_ocorrencia = models.CharField(max_length=128, blank=True, null=True)
    data_inicio_ultima_ocorrencia = models.DateField(blank=True, null=True)
    nome_carreira = models.CharField(max_length=64, blank=True, null=True)
    nome_funcao = models.CharField(max_length=64, blank=True, null=True)
    nome_classe = models.CharField(max_length=64, blank=True, null=True)
    nome_grau_provimento = models.CharField(max_length=1, blank=True, null=True)
    data_ultima_alteracao_funcional = models.DateField(blank=True, null=True)
    cargo = models.CharField(max_length=64, blank=True, null=True)
    tipo_jornada = models.CharField(max_length=32, blank=True, null=True)
    tipo_condicao = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vinculos_servidores'
