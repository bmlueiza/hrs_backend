from django.urls import path
import hrsapp.views.observacion_views as observacion_views


urlpatterns = [
    path(
        "api/observaciones/",
        observacion_views.ObservacionCreateListView.as_view(),
        name="lista_crear_observaciones",
    ),
    path(
        "api/observaciones/<int:pk>/",
        observacion_views.ObservacionDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_observacion",
    ),
    path(
        "api/pacientes/<int:id_paciente>/observaciones/",
        observacion_views.ObservacionByPacienteListView.as_view(),
        name="lista_observaciones_por_paciente",
    ),
]
