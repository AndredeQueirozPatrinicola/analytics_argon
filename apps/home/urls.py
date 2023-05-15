from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve



from apps.home import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='home'),

    path('projeto/', views.SobrenosView.as_view(), name='sobre-nos'),

    path('departamentos/', views.DepartamentosView.as_view(), name='departamentos'),

    path('graduacao/geral/', views.GraduacaoGeral.as_view(), name='graduacao'),

    path('graduacao/diversidade/', views.GraduacaoDiversidade.as_view(), name='graduacao'),

    path('graduacao/pesquisa/', views.GraduacaoPesquisa.as_view(), name='graduacao'),

    path('pos-graduacao/geral/', views.PosGraduacaoGeral.as_view(), name='graduacao'),

    path('pos-graduacao/diversidade/', views.PosGraduacaoDiversidade.as_view(), name='graduacao'),

    path('pos-graduacao/pesquisa/', views.PosGraduacaoPesquisa.as_view(), name='graduacao'),

    path('docentes/', views.DocenteView.as_view(), name='docentes'),

    path('docentes/<str:docente>/', views.DocenteView.as_view(), name='graduacao-docente'),

    path('departamentos/<str:sigla>', views.DepartamentoView.as_view(), name='docentes'),

    path('<str:sigla>/docente/<str:numero_lattes>', views.DocenteView.as_view(), name='docente'),
]
