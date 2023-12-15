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


# Leer un HistorialContacto de un paciente en específico
class HistorialContactoPacienteListView(generics.ListAPIView):
    serializer_class = HistorialContactoSerializer

    def get_queryset(self):
        paciente_id = self.kwargs["pk"]
        return HistorialContacto.objects.filter(paciente=paciente_id)
