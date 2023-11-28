from rest_framework import generics
from hrsapp.models.motivo import Motivo
from hrsapp.serializers.motivo_serializer import MotivoSerializer

# CRUD Motivo


# Crear y leer Motivos
class MotivoCreateListView(generics.ListCreateAPIView):
    queryset = Motivo.objects.all()
    serializer_class = MotivoSerializer


# Leer, actualizar y eliminar Motivos
class MotivoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Motivo.objects.all()
    serializer_class = MotivoSerializer
