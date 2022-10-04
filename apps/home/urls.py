from django.urls import path, re_path
from django.conf.urls import url 
from django.conf import settings
from django.views.static import serve



from apps.home import views

urlpatterns = [

    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

    # The home page
    path('', views.index, name='home'),

    path('departamentos', views.departamentos, name='departamentos'),

    path('departamentos/<str:sigla>', views.departamento, name='docentes'),

    path('<str:sigla>/docente/<str:parametro>', views.docente, name='docente'),

    path('teste/', views.testes),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
