from rest_framework import generics
from rest_framework.response import Response
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.serializers.asignacion_actividad_serializer import (
    AsignacionActividadSerializer,
)
from hrsapp.serializers.actividad_medica_serializer import ActividadMedicaSerializer

# CRUD AsignacionActividad


# Crear y leer Asignaciones de Actividad
class AsignacionActividadCreateListView(generics.ListCreateAPIView):
    queryset = AsignacionActividad.objects.all()
    serializer_class = AsignacionActividadSerializer


# Leer, editar y eliminar una AsignacionActividad en específico
class AsignacionActividadDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AsignacionActividad.objects.all()
    serializer_class = AsignacionActividadSerializer


# Leer las AsignacionActividad de un paciente en específico
class AsignacionActividadPacienteListView(generics.ListAPIView):
    serializer_class = AsignacionActividadSerializer

    def get_queryset(self):
        paciente_id = self.kwargs["pk"]
        return AsignacionActividad.objects.filter(paciente=paciente_id)


# Leer las actividades médicas de las AsignacionActividad de un paciente en específico que se encuentren con estado Asignada o No realizada
class AsignacionActividadPacientePendienteListView(generics.ListAPIView):
    serializer_class = ActividadMedicaSerializer

    def list(self, request, *args, **kwargs):
        paciente_id = self.kwargs["pk"]
        actividades_queryset = (
            AsignacionActividad.objects.filter(
                paciente=paciente_id,
                estado__in=[1, 4],
            )
            .values_list("actividad_medica__nombre", flat=True)
            .distinct()
        )

        return Response(actividades_queryset)
