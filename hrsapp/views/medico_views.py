from rest_framework import generics
from hrsapp.models.medico import Medico
from hrsapp.serializers.medico_serializer import MedicoSerializer

# CRUD Médico


# Crear y listar Medicos
class MedicoCreateListView(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

    def get_queryset(self):
        termino = self.request.query_params.get("termino", None)
        if termino:
            return Medico.buscar_medicos(termino)
        return super().get_queryset()


# Leer, actualizar y eliminar un Medico en específico
class MedicoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


# Obtener los médicos de una especialidad en específico
class MedicoEspecialidadListView(generics.ListAPIView):
    serializer_class = MedicoSerializer

    def get_queryset(self):
        especialidad = self.kwargs["especialidad"]
        return Medico.objects.filter(especialidad=especialidad)
