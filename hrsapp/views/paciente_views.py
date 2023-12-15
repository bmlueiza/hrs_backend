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


# Leer pacientes según su diagnóstico
class PacienteByDiagnosticoListView(generics.ListAPIView):
    serializer_class = PacienteSerializer

    def get_queryset(self):
        try:
            id_diagnostico = self.kwargs["diagnostico_id"]
            return Paciente.objects.filter(diagnosticos__id=id_diagnostico)
        except KeyError:
            return Paciente.objects.none()


# Leer pacientes según su riesgo
class PacienteByRiesgoListView(generics.ListAPIView):
    serializer_class = PacienteSerializer

    def get_queryset(self):
        try:
            riesgo = int(self.kwargs["riesgo"])
            return Paciente.objects.filter(riesgo=riesgo)
        except (KeyError, ValueError):
            return Paciente.objects.none()


# Funcion para obtener opciones de sexo
class PacienteSexoListView(APIView):
    def get(self, request):
        return Response(Paciente.SEXO_CHOICES)


# Funcion para obtener opciones de riesgo
class PacienteRiesgoListView(APIView):
    def get(self, request):
        return Response(Paciente.RIESGO_CHOICES)


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
