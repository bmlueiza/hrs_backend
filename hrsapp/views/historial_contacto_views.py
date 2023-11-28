from rest_framework import generics
from hrsapp.models.historial_contacto import HistorialContacto
from hrsapp.serializers.historial_contacto_serializer import (
    HistorialContactoSerializer,
)


# CRUD HistorialContacto


# Crear y leer Historiales de Contacto
class HistorialContactoCreateListView(generics.ListCreateAPIView):
    queryset = HistorialContacto.objects.all()
    serializer_class = HistorialContactoSerializer


# Leer, editar y eliminar un HistorialContacto en específico
class HistorialContactoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialContacto.objects.all()
    serializer_class = HistorialContactoSerializer
