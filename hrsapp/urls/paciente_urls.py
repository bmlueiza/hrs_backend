from django.urls import path
import hrsapp.views.paciente_views as paciente_views

urlpatterns = [
    path(
        "api/pacientes/",
        paciente_views.PacienteCreateListView.as_view(),
        name="lista_crear_pacientes",
    ),
    path(
        "api/pacientes/<int:pk>/",
        paciente_views.PacienteDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_paciente",
    ),
    path(
        "api/pacientes/<int:paciente_id>/observaciones/",
        paciente_views.PacienteObservacionesView.as_view(),
        name="observaciones_paciente",
    ),
]
