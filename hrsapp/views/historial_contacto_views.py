from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
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


# Obtener las opciones de tipo_motivo
class HistorialContactoTipoMotivoListView(APIView):
    def get(self, request):
        return Response(HistorialContacto.TIPO_MOTIVO_CHOICES)


# Obtener las opciones de resultado_contacto
class HistorialContactoResultadoContactoListView(APIView):
    def get(self, request):
        return Response(HistorialContacto.RESULTADO_CONTACTO_CHOICES)
