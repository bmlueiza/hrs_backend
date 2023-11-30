from django.urls import path
import hrsapp.views.diagnostico_views as diagnostico_views

urlpatterns = [
    path(
        "api/diagnosticos/",
        diagnostico_views.DiagnosticoCreateListView.as_view(),
        name="lista_crear_diagnosticos",
    ),
    path(
        "api/diagnosticos/<int:pk>/",
        diagnostico_views.DiagnosticoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_diagnostico",
    ),
]
