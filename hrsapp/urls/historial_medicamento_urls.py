from django.urls import path
import hrsapp.views.historial_medicamento_views as historial_medicamento_views


urlpatterns = [
    path(
        "api/historial_medicamentos/",
        historial_medicamento_views.HistorialMedicamentoCreateListView.as_view(),
        name="lista_crear_historiales_medicamento",
    ),
    path(
        "api/historial_medicamentos/<int:pk>/",
        historial_medicamento_views.HistorialMedicamentoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_historial_medicamento",
    ),
    path(
        "api/historial_medicamentos/paciente/<int:pk>/",
        historial_medicamento_views.HistorialMedicamentoPacienteListView.as_view(),
        name="lista_historiales_medicamento_paciente",
    ),
    path(
        "api/historial_medicamentos/paciente/<int:pk>/medicamentos/",
        historial_medicamento_views.MedicamentosPacienteListView.as_view(),
        name="lista_medicamentos_paciente",
    ),
]
