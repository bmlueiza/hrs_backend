from django.urls import path
import hrsapp.views.motivo_views as motivo_views

urlpatterns = [
    path(
        "api/motivos/",
        motivo_views.MotivoCreateListView.as_view(),
        name="lista_crear_motivos",
    ),
    path(
        "api/motivos/<int:pk>/",
        motivo_views.MotivoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_motivo",
    ),
]
