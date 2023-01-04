from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve 
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),             # UI Kits Html files
    # path("api/", include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT
        })
    ]