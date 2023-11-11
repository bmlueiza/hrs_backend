from django.urls import path
import hrsapp.views.paciente_views as paciente_views

urlpatterns = [
    path(
        "api/pacientes/",
        paciente_views.PacienteListView.as_view(),
        name="lista_pacientes",
    ),
    path(
        "api/pacientes/<int:pk>/",
        paciente_views.PacienteDetailView.as_view(),
        name="detalle_paciente",
    ),
    path(
        "api/pacientes/crear/",
        paciente_views.PacienteCreateView.as_view(),
        name="crear_paciente",
    ),
    # Otras rutas relacionadas con pacientes
]
