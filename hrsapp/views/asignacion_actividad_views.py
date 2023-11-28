from rest_framework import generics
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.serializers.asignacion_actividad_serializer import (
    AsignacionActividadSerializer,
)

# CRUD AsignacionActividad


# Crear y leer Asignaciones de Actividad
class AsignacionActividadCreateListView(generics.ListCreateAPIView):
    queryset = AsignacionActividad.objects.all()
    serializer_class = AsignacionActividadSerializer


# Leer, editar y eliminar una AsignacionActividad en específico
class AsignacionActividadDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AsignacionActividad.objects.all()
    serializer_class = AsignacionActividadSerializer
