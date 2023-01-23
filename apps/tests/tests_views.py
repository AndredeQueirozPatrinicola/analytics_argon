import requests
from django.test import TestCase, Client, RequestFactory

from apps.home import models
from apps.home import views
from services.populadb import Docentes

class ViewsTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        self.url="" 

    def test_get_status_code(self):
        response = self.client.get(self.url)
        status = response.status_code
        self.assertEquals(status, 200)

    def test_post_status_code(self):
        response = self.client.post(self.url, {"nome": "Teste", "senha" : "Teste123"})
        status = response.status_code
        self.assertEquals(status, 405)

    def test_delete_status_code(self):
        response = self.client.delete(self.url, {"nome": "Teste", "senha" : "Teste123"})
        status = response.status_code
        self.assertEquals(status, 405)
    
    def test_put_status_code(self):
        response = self.client.put(self.url, {"nome": "Teste", "senha" : "Teste123"})
        status = response.status_code
        self.assertEquals(status, 405)
        

class IndexViewTestCase(ViewsTestCase):
        
    def setUp(self) -> None:
        super().setUp()
        self.url="/"
        
class DocenteViewTestCase(ViewsTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.numero_lattes = "4985145537112489"
        self.departamento = "FLG"
        self.url=f"/{self.departamento}/docente/{self.numero_lattes}"
        self.API = Docentes.ApiDocente(self.numero_lattes)
        self.docente = models.Docente.objects.create(
            docente_id=self.url,
            api_docente=self.API.pega_api_docente(),
            api_programas=self.API.pega_api_programas(),
            api_docentes=self.API.pega_api_docentes()
        )

    def test_queries(self):
        queries = views.DocenteView().queries(self.numero_lattes)
        api_docente = queries.get('api_docente')
        api_programas = queries.get('api_programas')  
        api_docentes = queries.get('api_docentes')
        if not api_docente or not api_programas or not api_docentes:
            raise ValueError("Valores de api incorretos")

    def test_get_content_type(self):
        request = self.factory.get(self.url)
        response = views.DocenteView.as_view()(request, self.departamento, self.numero_lattes)
        content_type = response.headers.get("Content-Type")
        if "text/html;" not in content_type:
            raise Exception("Não retornou HTML")


# class DocenteViewAposentadoTestCase(DocenteViewTestCase):
    
#     def setUp(self) -> None:
#         super().setUp()
#         self.numero_lattes = '6454039195387336'
#         self.departamento = 'FLH'
#         self.url = f'/{self.departamento}/docente/{self.numero_lattes}'
#         self.API = Docentes.ApiDocente(self.numero_lattes)
#         self.docente = models.Docente.objects.create(
#             docente_id=self.url,
#             api_docente=self.API.pega_api_docente(),
#             api_programas=self.API.pega_api_programas(),
#             api_docentes=self.API.pega_api_docentes()
#         )
        

            
         
        



    

    
        

    
    