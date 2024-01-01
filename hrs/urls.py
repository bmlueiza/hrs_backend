"""
URL configuration for hrs project.

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
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", include_docs_urls(title="HRS API Documentation")),
    # Rutas de acceso desde la app hrsapp
    # Rutas de acciones de gestores
    path("hrsapp/", include("hrsapp.urls.accion_gestor_urls")),
    # Rutas de actividades medicas
    path("hrsapp/", include("hrsapp.urls.actividad_medica_urls")),
    # Rutas de asignaciones de actividades
    path("hrsapp/", include("hrsapp.urls.asignacion_actividad_urls")),
    # Rutas de diagnosticos
    path("hrsapp/", include("hrsapp.urls.diagnostico_urls")),
    # Rutas de especialidades medicas
    path("hrsapp/", include("hrsapp.urls.especialidad_medica_urls")),
    # Rutas de gestores
    path("hrsapp/", include("hrsapp.urls.gestor_urls")),
    # Rutas de historiales de contacto
    path("hrsapp/", include("hrsapp.urls.historial_contacto_urls")),
    # Rutas de seguimiento de medicamentos
    path("hrsapp/", include("hrsapp.urls.seguimiento_medicamento_urls")),
    # Rutas de medicamentos
    path("hrsapp/", include("hrsapp.urls.medicamento_urls")),
    # Rutas de medicos
    path("hrsapp/", include("hrsapp.urls.medico_urls")),
    # Rutas de observaciones
    path("hrsapp/", include("hrsapp.urls.observacion_urls")),
    # Rutas de pacientes
    path("hrsapp/", include("hrsapp.urls.paciente_urls")),
    # Rutas de recomendaciones
    path("hrsapp/", include("hrsapp.urls.recomendacion_urls")),
    # Rutas de login
    path("hrsapp/", include("hrsapp.urls.login_urls")),
    # Otras rutas principales
]
