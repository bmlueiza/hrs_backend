from django.urls import path
import hrsapp.views.diagnostico_views as diagnostico_views

urlpatterns = [
    path(
        "api/diagnosticos/",
        diagnostico_views.DiagnosticoListView.as_view(),
        name="lista_diagnosticos",
    ),
    path(
        "api/diagnosticos/<int:pk>/",
        diagnostico_views.DiagnosticoDetailView.as_view(),
        name="detalle_diagnostico",
    ),
    path(
        "api/diagnosticos/create/",
        diagnostico_views.DiagnosticoCreateView.as_view(),
        name="crear_diagnostico",
    ),
]
