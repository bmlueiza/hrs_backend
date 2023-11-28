from django.urls import path
import hrsapp.views.resultado_contacto_views as resultado_contacto_views


urlpatterns = [
    path(
        "api/resultados_contacto/",
        resultado_contacto_views.ResultadoContactoCreateListView.as_view(),
        name="lista_crear_resultados_contacto",
    ),
    path(
        "api/resultados_contacto/<int:pk>/",
        resultado_contacto_views.ResultadoContactoDetailUpdateDeleteView.as_view(),
        name="detalle_actualizar_eliminar_resultado_contacto",
    ),
]
