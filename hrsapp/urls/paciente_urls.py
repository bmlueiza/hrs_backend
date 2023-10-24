from django.urls import path
from hrsapp.views.paciente_views import ListaPacientes

urlpatterns = [
    path("api/pacientes/", ListaPacientes.as_view(), name="lista_pacientes"),
    # path('api/pacientes/<int:pk>/', views.DetallePaciente.as_view(), name='detalle_paciente'),
    # Otras rutas relacionadas con pacientes
]
