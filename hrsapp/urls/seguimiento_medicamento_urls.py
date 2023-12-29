from django.urls import path
import hrsapp.views.seguimiento_medicamento_views as seguimiento_medicamento_views


urlpatterns = [
    path(
        "api/seguimiento_medicamentos/",
        seguimiento_medicamento_views.SeguimientoMedicamentoCreateListView.as_view(),
        name="lista_crear_seguimiento_medicamentos",
    ),
    path(
        "api/seguimiento_medicamentos/<int:pk>/",
        seguimiento_medicamento_views.SeguimientoMedicamentoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_seguimiento_medicamento",
    ),
    path(
        "api/seguimiento_medicamentos/paciente/<int:pk>/",
        seguimiento_medicamento_views.SeguimientoMedicamentoPacienteListView.as_view(),
        name="lista_seguimiento_medicamentos_paciente",
    ),
    path(
        "api/seguimiento_medicamentos/paciente/<int:pk>/medicamentos/",
        seguimiento_medicamento_views.MedicamentosPacienteListView.as_view(),
        name="lista_medicamentos_paciente",
    ),
    path(
        "api/seguimiento_medicamentos/estados/",
        seguimiento_medicamento_views.SeguimientoMedicamentoEstadoListView.as_view(),
        name="lista_estado_seguimiento_medicamento",
    ),
]
