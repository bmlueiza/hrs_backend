from django.urls import path
import hrsapp.views.recomendacion_views as recomendacion_views

urlpatterns = [
    path(
        "api/recomendaciones/",
        recomendacion_views.RecomendacionListView.as_view(),
        name="lista_crear_recomendaciones",
    ),
    path(
        "api/recomendaciones/<int:pk>/",
        recomendacion_views.RecomendacionDetailView.as_view(),
        name="detalle_actualizar_eliminar_recomendacion",
    ),
]
