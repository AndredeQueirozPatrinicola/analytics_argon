from django.urls import path, re_path
from django.conf.urls import url 
from django.conf import settings
from django.views.static import serve



from apps.home import views

urlpatterns = [

    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

    # The home page
    path('', views.IndexView.as_view(), name='home'),

    path('sobre-nos', views.SobrenosView.as_view(), name='sobre-nos'),

    path('departamentos', views.DepartamentosView.as_view(), name='departamentos'),

    path('departamentos/<str:sigla>', views.DepartamentoView.as_view(), name='docentes'),

    path('<str:sigla>/docente/<str:numero_lattes>', views.DocenteView.as_view(), name='docente'),

    # # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
