"""
URL configuration for MONSTER_APP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from MONSTER_APP.views import inicio, inicioAdmin,adm_inicio
from django.conf.urls import handler404
from django.views.i18n import JavaScriptCatalog
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [

] + staticfiles_urlpatterns()

urlpatterns = [
    ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("adm/", inicioAdmin, name="inicio-admin"),
    path("adm_inicio/", adm_inicio, name="adm_inicio"),
    path("", include("Aplicaciones.Protocolo_Metodos.urls")),
    path("", include("Aplicaciones.Secuencias.urls")),
    path("", include("Aplicaciones.Protocolo_Muestras.urls")),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path("select2/", include("django_select2.urls")),
    path("", include("Aplicaciones.perfiles.urls")),
    path('api/chart/finalizados/metodos/<int:year>/', views.chart_finalizados_metodos, name='chart_metodos'),
    path('api/chart/finalizados/proceso/<int:year>/', views.chart_finalizados_proceso, name='chart_proceso'),
    path('api/chart/motivos/metodos/<int:year>/', views.chart_motivos_metodos, name='chart_motivos_metodos'),
    path('api/chart/motivos/proceso/<int:year>/', views.chart_motivos_proceso, name='chart_motivos_proceso'),





 

    #path("incia-sesion/", SignOutView.as_view(), name="inicio-sign_out"),

    

]


    

