from django.urls import path
import hrsapp.views.medico_views as medico_views

urlpatterns = [
    path(
        "api/medicos/",
        medico_views.MedicoListView.as_view(),
        name="lista_medicos",
    ),
    path(
        "api/medicos/<int:pk>/",
        medico_views.MedicoDetailView.as_view(),
        name="detalle_medico",
    ),
]
