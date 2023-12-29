from django.urls import path
import hrsapp.views.medico_views as medico_views

urlpatterns = [
    path(
        "api/medicos/",
        medico_views.MedicoCreateListView.as_view(),
        name="lista_crear_medicos",
    ),
    path(
        "api/medicos/<int:pk>/",
        medico_views.MedicoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_medico",
    ),
    path(
        "api/medicos/especialidad/<str:especialidad>/",
        medico_views.MedicoEspecialidadListView.as_view(),
        name="medicos_especialidad",
    ),
]
