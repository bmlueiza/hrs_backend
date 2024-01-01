from django.urls import path
import hrsapp.views.historial_contacto_views as historial_contacto_views


urlpatterns = [
    path(
        "api/historial_contactos/",
        historial_contacto_views.HistorialContactoCreateListView.as_view(),
        name="lista_crear_historial_contactos",
    ),
    path(
        "api/historial_contactos/<int:pk>/",
        historial_contacto_views.HistorialContactoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_historial_contacto",
    ),
    path(
        "api/historial_contactos/paciente/<int:pk>/",
        historial_contacto_views.HistorialContactoPacienteListView.as_view(),
        name="lista_historial_contactos_paciente",
    ),
    path(
        "api/historial_contactos/tipo_motivo/",
        historial_contacto_views.HistorialContactoTipoMotivoListView.as_view(),
        name="lista_tipo_motivo",
    ),
    path(
        "api/historial_contactos/resultado_contacto/",
        historial_contacto_views.HistorialContactoResultadoContactoListView.as_view(),
        name="lista_resultado_contacto",
    ),
]
