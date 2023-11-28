from django.urls import path
import hrsapp.views.accion_gestor_views as accion_gestor_views

urlpatterns = [
    path(
        "api/acciones_gestor/",
        accion_gestor_views.AccionGestorCreateListView.as_view(),
        name="lista_crear_acciones_gestor",
    ),
    path(
        "api/acciones_gestor/<int:pk>/",
        accion_gestor_views.AccionGestorDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_accion_gestor",
    ),
]
