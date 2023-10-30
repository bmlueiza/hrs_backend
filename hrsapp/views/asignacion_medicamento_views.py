from rest_framework import generics
from hrsapp.models.asignacion_medicamento import AsignacionMedicamento
from hrsapp.serializers.asignacion_medicamento_serializer import (
    AsignacionMedicamentoSerializer,
)

# CRUD AsignacionMedicamento


# Crear AsignacionMedicamento
class AsignacionMedicamentoCreateView(generics.CreateAPIView):
    queryset = AsignacionMedicamento.objects.all()
    serializer_class = AsignacionMedicamentoSerializer


# Leer Asignaciones Medicamentos
class AsignacionMedicamentoListView(generics.ListAPIView):
    queryset = AsignacionMedicamento.objects.all()
    serializer_class = AsignacionMedicamentoSerializer


# Leer una AsignacionMedicamento en específico
class AsignacionMedicamentoDetailView(generics.RetrieveAPIView):
    queryset = AsignacionMedicamento.objects.all()
    serializer_class = AsignacionMedicamentoSerializer


# Actualizar AsignacionMedicamento
class AsignacionMedicamentoUpdateView(generics.UpdateAPIView):
    queryset = AsignacionMedicamento.objects.all()
    serializer_class = AsignacionMedicamentoSerializer


# Eliminar AsignacionMedicamento
class AsignacionMedicamentoDeleteView(generics.DestroyAPIView):
    queryset = AsignacionMedicamento.objects.all()
    serializer_class = AsignacionMedicamentoSerializer
