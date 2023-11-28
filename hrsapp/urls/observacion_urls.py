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
]
