from django.urls import path
import hrsapp.views.recomendacion_views as recomendacion_views

urlpatterns = [
    path(
        "api/recomendaciones/gestor/<int:gestor_id>/",
        recomendacion_views.RecomendacionGestorListView.as_view(),
        name="recomendaciones_gestor",
    ),
    path(
        "api/recomendaciones/paciente/<int:paciente_id>/",
        recomendacion_views.RecomendacionPacienteListView.as_view(),
        name="recomendaciones_paciente",
    ),
]
