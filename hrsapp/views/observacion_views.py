from rest_framework import generics
from hrsapp.models.observacion import Observacion
from hrsapp.serializers.observacion_serializer import ObservacionSerializer

# CRUD Observacion


# Crear y leer Observaciones
class ObservacionCreateListView(generics.ListCreateAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer


# Leer, editar y eliminar una Observacion en específico
class ObservacionDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer


# Leer observaciones de un paciente en específico (por su id)
class ObservacionByPacienteListView(generics.ListAPIView):
    serializer_class = ObservacionSerializer

    def get_queryset(self):
        id_paciente = self.kwargs["id_paciente"]
        return Observacion.objects.filter(paciente=id_paciente)
