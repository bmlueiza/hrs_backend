from django.urls import path
import hrsapp.views.recomendacion_views as recomendacion_views

urlpatterns = [
    path(
        "api/recomendaciones/",
        recomendacion_views.RecomendacionListView.as_view(),
        name="lista_recomendaciones",
    ),
]
