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
    path(
        "api/gestores/create",
        gestor_views.GestorCreateView.as_view(),
        name="crear_gestor",
    ),
    path(
        "api/gestores/update/<int:pk>/",
        gestor_views.GestorUpdateView.as_view(),
        name="actualizar_gestor",
    ),
    path(
        "api/gestores/delete/<int:pk>/",
        gestor_views.GestorDeleteView.as_view(),
        name="borrar_gestor",
    ),
]
