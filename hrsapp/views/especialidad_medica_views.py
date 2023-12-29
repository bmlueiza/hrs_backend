from rest_framework import generics
from hrsapp.models.especialidad_medica import EspecialidadMedica
from hrsapp.serializers.especialidad_medica_serializer import (
    EspecialidadMedicaSerializer,
)

# CRUD Especialidad Médica


# Crear y listar Especialidades Médicas
class EspecialidadMedicaCreateListView(generics.ListCreateAPIView):
    queryset = EspecialidadMedica.objects.all()
    serializer_class = EspecialidadMedicaSerializer

    def get_queryset(self):
        termino = self.request.query_params.get("termino", None)
        if termino:
            return EspecialidadMedica.buscar_especialidades_medicas(termino)
        return super().get_queryset()


# Leer, actualizar y eliminar una Especialidad Médica en específico
class EspecialidadMedicaDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EspecialidadMedica.objects.all()
    serializer_class = EspecialidadMedicaSerializer
