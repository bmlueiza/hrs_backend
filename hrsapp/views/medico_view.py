from rest_framework import generics
from hrsapp.models.medico import Medico
from hrsapp.serializers.medico_serializer import MedicoSerializer

# CRUD Médico


# Crear Médico
class MedicoCreateView(generics.CreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


# Leer Médicos
class MedicoListView(generics.ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


# Leer un Médico en específico
class MedicoDetailView(generics.RetrieveAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


# Actualizar Médico
class MedicoUpdateView(generics.UpdateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


# Eliminar Médico
class MedicoDeleteView(generics.DestroyAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
