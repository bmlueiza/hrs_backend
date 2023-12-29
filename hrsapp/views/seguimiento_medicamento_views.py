from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from hrsapp.models.seguimiento_medicamento import SeguimientoMedicamento
from hrsapp.serializers.seguimiento_medicamento_serializer import (
    SeguimientoMedicamentoSerializer,
)


# CRUD SeguimientoMedicamento


# Crear y leer Seguimiento de Medicamentos
class SeguimientoMedicamentoCreateListView(generics.ListCreateAPIView):
    queryset = SeguimientoMedicamento.objects.all()
    serializer_class = SeguimientoMedicamentoSerializer


# Leer, editar y eliminar un SeguimientoMedicamento en específico
class SeguimientoMedicamentoDetailUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = SeguimientoMedicamento.objects.all()
    serializer_class = SeguimientoMedicamentoSerializer


# Leer Seguimiento Medicamentos de un paciente en específico
class SeguimientoMedicamentoPacienteListView(generics.ListAPIView):
    serializer_class = SeguimientoMedicamentoSerializer

    def get_queryset(self):
        paciente_id = self.kwargs["pk"]
        return SeguimientoMedicamento.objects.filter(paciente=paciente_id)


# Leer medicamento de Seguimiento Medicamentos de un paciente en específico
class MedicamentosPacienteListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        paciente_id = kwargs["pk"]
        # Obtén una lista de nombres de medicamentos para el paciente específico
        nombres_medicamentos = SeguimientoMedicamento.objects.filter(
            paciente=paciente_id
        ).values_list("medicamento__nombre", flat=True)

        # Devuelve la lista de nombres como parte de la respuesta JSON
        return Response({"nombres_medicamentos": list(nombres_medicamentos)})


# Obtener opciones de estado
class SeguimientoMedicamentoEstadoListView(APIView):
    def get(self, request):
        return Response(SeguimientoMedicamento.ESTADO_CHOICES)
