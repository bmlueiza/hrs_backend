from django.urls import path
import hrsapp.views.gestor_views as gestor_views

urlpatterns = [
    path(
        "api/gestores/",
        gestor_views.GestorCreateListView.as_view(),
        name="lista_crear_gestores",
    ),
    path(
        "api/gestores/<int:pk>/",
        gestor_views.GestorDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_gestor",
    ),
    path(
        "api/gestores/username/<str:username>/",
        gestor_views.GestorUsernameView.as_view(),
        name="gestor_username",
    ),
]
