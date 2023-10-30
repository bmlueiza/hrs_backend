from rest_framework import generics
from hrsapp.models.medicamento import Medicamento
from hrsapp.serializers.medicamento_serializer import MedicamentoSerializer

# CRUD Medicamento


# Crear Medicamento
class MedicamentoCreateView(generics.CreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


# Leer Medicamentos
class MedicamentoListView(generics.ListAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


# Leer un Medicamento en específico
class MedicamentoDetailView(generics.RetrieveAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


# Actualizar Medicamento
class MedicamentoUpdateView(generics.UpdateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


# Eliminar Medicamento
class MedicamentoDeleteView(generics.DestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
