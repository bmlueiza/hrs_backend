from rest_framework import generics
from hrsapp.models.seguimiento_paciente import SeguimientoPaciente
from hrsapp.serializers.seguimiento_paciente_serializer import (
    SeguimientoPacienteSerializer,
)

# CRUD Seguimiento Paciente


# Crear SeguimientoPaciente
class SeguimientoPacienteCreateView(generics.CreateAPIView):
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer


# Leer SeguimientoPacientes
class SeguimientoPacienteListView(generics.ListAPIView):
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer


# Leer un SeguimientoPaciente en específico
class SeguimientoPacienteDetailView(generics.RetrieveAPIView):
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer


# Actualizar SeguimientoPaciente
class SeguimientoPacienteUpdateView(generics.UpdateAPIView):
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer


# Eliminar SeguimientoPaciente
class SeguimientoPacienteDeleteView(generics.DestroyAPIView):
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer
