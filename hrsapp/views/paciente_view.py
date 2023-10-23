from rest_framework import generics
from models.paciente import Paciente
from serializers.paciente_serializer import PacienteSerializer

# CRUD Paciente


# Crear
class CrearPacientes(generics.CreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Leer
class ListaPacientes(generics.ListAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Actualizar
class PacienteUpdateView(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Eliminar
class PacienteDeleteView(generics.DestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
