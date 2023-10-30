from django.urls import path
import hrsapp.views.medicamento_views as medicamento_views

urlpatterns = [
    path(
        "api/medicamentos/",
        medicamento_views.MedicamentoListView.as_view(),
        name="lista_medicamentos",
    ),
    path(
        "api/medicamentos/<int:pk>/",
        medicamento_views.MedicamentoDetailView.as_view(),
        name="detalle_medicamento",
    ),
]
