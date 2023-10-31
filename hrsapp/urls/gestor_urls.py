from django.urls import path
import hrsapp.views.gestor_views as gestor_views

urlpatterns = [
    path(
        "api/gestores/",
        gestor_views.GestorListView.as_view(),
        name="lista_gestores",
    ),
    path(
        "api/gestores/<int:pk>/",
        gestor_views.GestorDetailView.as_view(),
        name="detalle_gestor",
    ),
]
