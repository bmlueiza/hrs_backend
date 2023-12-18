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
]
