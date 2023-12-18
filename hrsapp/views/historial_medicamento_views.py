from rest_framework import generics
from rest_framework.response import Response
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


# Leer medicamento de Historial Medicamentos de un paciente en específico
class MedicamentosPacienteListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        paciente_id = kwargs["pk"]
        # Obtén una lista de nombres de medicamentos para el paciente específico
        nombres_medicamentos = HistorialMedicamento.objects.filter(
            paciente=paciente_id
        ).values_list("medicamento__nombre", flat=True)

        # Devuelve la lista de nombres como parte de la respuesta JSON
        return Response({"nombres_medicamentos": list(nombres_medicamentos)})
