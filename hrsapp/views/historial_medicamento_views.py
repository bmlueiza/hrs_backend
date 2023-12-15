from rest_framework import generics
from hrsapp.models.historial_medicamento import HistorialMedicamento
from hrsapp.serializers.historial_medicamento_serializer import (
    HistorialMedicamentoSerializer,
)


# CRUD HistorialMedicamento


# Crear y leer Historiales de Medicamento
class HistorialMedicamentoCreateListView(generics.ListCreateAPIView):
    queryset = HistorialMedicamento.objects.all()
    serializer_class = HistorialMedicamentoSerializer


# Leer, editar y eliminar un HistorialMedicamento en específico
class HistorialMedicamentoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialMedicamento.objects.all()
    serializer_class = HistorialMedicamentoSerializer


# Leer Historial Medicamentos de un paciente en específico
class HistorialMedicamentoPacienteListView(generics.ListAPIView):
    serializer_class = HistorialMedicamentoSerializer

    def get_queryset(self):
        paciente_id = self.kwargs["pk"]
        return HistorialMedicamento.objects.filter(paciente=paciente_id)
