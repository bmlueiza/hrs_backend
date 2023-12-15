from django.urls import path
import hrsapp.views.historial_medicamento_views as historial_medicamento_views


urlpatterns = [
    path(
        "api/historiales_medicamento/",
        historial_medicamento_views.HistorialMedicamentoCreateListView.as_view(),
        name="lista_crear_historiales_medicamento",
    ),
    path(
        "api/historiales_medicamento/<int:pk>/",
        historial_medicamento_views.HistorialMedicamentoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_historial_medicamento",
    ),
    path(
        "api/historial_medicamento/paciente/<int:pk>/",
        historial_medicamento_views.HistorialMedicamentoPacienteListView.as_view(),
        name="lista_historiales_medicamento_paciente",
    ),
]
