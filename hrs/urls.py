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

urlpatterns = [
    path("admin/", admin.site.urls),
    # Rutas de pacientes desde la app hrsapp
    path("hrsapp/", include("hrsapp.urls.paciente_urls")),
    # Rutas de recomendaciones desde la app hrsapp
    path("hrsapp/", include("hrsapp.urls.recomendacion_urls")),
    # Rutas de diagnosticos desde la app hrsapp
    path("hrsapp/", include("hrsapp.urls.diagnostico_urls")),
    # Rutas de medicamentos desde la app hrsapp
    path("hrsapp/", include("hrsapp.urls.medicamento_urls")),
    # Rutas de medicos desde la app hrsapp
    path("hrsapp/", include("hrsapp.urls.medico_urls")),
    # Otras rutas principales
]
