from rest_framework import generics
from hrsapp.models.medicamento import Medicamento
from hrsapp.serializers.medicamento_serializer import MedicamentoSerializer

# CRUD Medicamento


# Crear y listar Medicamentos
class MedicamentoCreateListView(generics.ListCreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


# Leer, actualizar y eliminar un Medicamento en específico
class MedicamentoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
