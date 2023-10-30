from django.urls import path
import hrsapp.views.paciente_views as Pacienteviews

urlpatterns = [
    path(
        "api/pacientes/",
        Pacienteviews.PacienteListView.as_view(),
        name="lista_pacientes",
    ),
    path(
        "api/pacientes/<int:pk>/",
        Pacienteviews.PacienteDetailView.as_view(),
        name="detalle_paciente",
    ),
    # Otras rutas relacionadas con pacientes
]
