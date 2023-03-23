#  AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacao='ativo').values('estadoNascimento').annotate(count=Count('*')).order_by('estadoNascimento')

from rest_framework import views
from rest_framework.response import Response

import json

class Teste(views.APIView):

    def get(self, *args, **kwargs):

        return Response({"ola":"Mundo"})