from django.urls import path
import hrsapp.views.medicamento_views as medicamento_views

urlpatterns = [
    path(
        "api/medicamentos/",
        medicamento_views.MedicamentoCreateListView.as_view(),
        name="lista_crear_medicamentos",
    ),
    path(
        "api/medicamentos/<int:pk>/",
        medicamento_views.MedicamentoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_medicamentos",
    ),
]
