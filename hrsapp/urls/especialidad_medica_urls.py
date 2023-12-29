from django.urls import path
import hrsapp.views.especialidad_medica_views as especialidad_medica_views

urlpatterns = [
    path(
        "api/especialidades_medicas/",
        especialidad_medica_views.EspecialidadMedicaCreateListView.as_view(),
        name="lista_crear_especialidades_medicas",
    ),
    path(
        "api/especialidades_medicas/<int:pk>/",
        especialidad_medica_views.EspecialidadMedicaDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_especialidad_medica",
    ),
]
