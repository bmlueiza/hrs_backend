from rest_framework import generics
from hrsapp.models.actividad_medica import ActividadMedica
from hrsapp.serializers.actividad_medica_serializer import (
    ActividadMedicaSerializer,
)

# CRUD ActividadMedica


# Crear y leer Actividades Medicas
class ActividadMedicaCreateListView(generics.ListCreateAPIView):
    queryset = ActividadMedica.objects.all()
    serializer_class = ActividadMedicaSerializer


# Leer, editar y eliminar una ActividadMedica en específico
class ActividadMedicaDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActividadMedica.objects.all()
    serializer_class = ActividadMedicaSerializer
