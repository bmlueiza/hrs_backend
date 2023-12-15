from django.urls import path
import hrsapp.views.asignacion_actividad_views as asignacion_actividad_views


urlpatterns = [
    path(
        "api/asignacion_actividades/",
        asignacion_actividad_views.AsignacionActividadCreateListView.as_view(),
        name="lista_crear_asignacion_actividades",
    ),
    path(
        "api/asignacion_actividades/<int:pk>/",
        asignacion_actividad_views.AsignacionActividadDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_asignacion_actividad",
    ),
    path(
        "api/asignacion_actividades/paciente/<int:pk>/",
        asignacion_actividad_views.AsignacionActividadPacienteListView.as_view(),
        name="lista_asignacion_actividades_paciente",
    ),
    path(
        "api/asignacion_actividades/paciente/<int:pk>/pendientes/",
        asignacion_actividad_views.AsignacionActividadPacientePendienteListView.as_view(),
        name="lista_asignacion_actividades_paciente_pendientes",
    ),
]
