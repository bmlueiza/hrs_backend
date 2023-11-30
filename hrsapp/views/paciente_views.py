from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from hrsapp.models.paciente import Paciente
from hrsapp.serializers.paciente_serializer import PacienteSerializer
from hrsapp.models.observacion import Observacion
from hrsapp.serializers.observacion_serializer import ObservacionSerializer

# CRUD Paciente


# Crear y leer Pacientes
class PacienteCreateListView(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_queryset(self):
        termino = self.request.query_params.get("termino", None)
        if termino:
            return Paciente.buscar_pacientes(termino)
        return super().get_queryset()


# Leer, editar y eliminar un Paciente en específico
class PacienteDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class PacienteObservacionesView(APIView):
    def get(self, request, paciente_id):
        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            return Response(
                {"error": "Paciente no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        observaciones = Observacion.objects.filter(paciente=paciente)
        observaciones_serializer = ObservacionSerializer(observaciones, many=True)

        paciente_serializer = PacienteSerializer(paciente)
        data = {
            "paciente": paciente_serializer.data,
            "observaciones": observaciones_serializer.data,
        }

        return Response(data)
