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
        "api/pacientes/diagnostico/<int:diagnostico_id>/",
        paciente_views.PacienteByDiagnosticoListView.as_view(),
        name="pacientes_por_diagnostico",
    ),
    path(
        "api/pacientes/riesgo/<int:riesgo>/",
        paciente_views.PacienteByRiesgoListView.as_view(),
        name="pacientes_por_riesgo",
    ),
    path(
        "api/pacientes/sexos/",
        paciente_views.PacienteSexoListView.as_view(),
        name="opciones_sexo",
    ),
    path(
        "api/pacientes/riesgos/",
        paciente_views.PacienteRiesgoListView.as_view(),
        name="opciones_riesgo",
    ),
    path(
        "api/pacientes/<int:pk>/agregar-diagnosticos/",
        paciente_views.PacienteDiagnosticoAddView.as_view(),
        name="agregar_diagnosticos_paciente",
    ),
]
