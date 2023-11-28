from django.urls import path
import hrsapp.views.actividad_medica_views as actividad_medica_views

urlpatterns = [
    path(
        "api/actividades_medicas/",
        actividad_medica_views.ActividadMedicaCreateListView.as_view(),
        name="lista_crear_actividades_medicas",
    ),
    path(
        "api/actividades_medicas/<int:pk>/",
        actividad_medica_views.ActividadMedicaDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_actividad_medica",
    ),
]
