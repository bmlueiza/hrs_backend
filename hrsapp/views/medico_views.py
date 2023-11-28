from rest_framework import generics
from hrsapp.models.medico import Medico
from hrsapp.serializers.medico_serializer import MedicoSerializer

# CRUD Médico


# Crear y listar Medicos
class MedicoCreateListView(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


# Leer, actualizar y eliminar un Medico en específico
class MedicoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
