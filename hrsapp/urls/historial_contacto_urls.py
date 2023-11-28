from django.urls import path
import hrsapp.views.historial_contacto_views as historial_contacto_views


urlpatterns = [
    path(
        "api/historiales_contacto/",
        historial_contacto_views.HistorialContactoCreateListView.as_view(),
        name="lista_crear_historiales_contacto",
    ),
    path(
        "api/historiales_contacto/<int:pk>/",
        historial_contacto_views.HistorialContactoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_historial_contacto",
    ),
]
