from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from hrsapp.models.paciente import Paciente
from hrsapp.serializers.paciente_serializer import PacienteSerializer
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.serializers.diagnostico_serializer import Diagnostico

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


# Añadir diagnósticos a un paciente sin eliminar los anteriores
class PacienteDiagnosticoAddView(APIView):
    def put(self, request, pk):
        try:
            paciente = Paciente.objects.get(pk=pk)
            diagnostico_id = request.data.get("diagnostico", None)

            if diagnostico_id:
                # Filtrar solo los diagnósticos existentes en la base de datos
                diagnostico_existente = Diagnostico.objects.filter(id=diagnostico_id)

                # Agregar nuevos diagnósticos al paciente sin eliminar los anteriores
                paciente.diagnosticos.add(*diagnostico_existente)
                paciente.save()

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Paciente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Pacientes por gestor
class PacienteByGestorListView(generics.ListAPIView):
    serializer_class = PacienteSerializer

    def get_queryset(self):
        try:
            id_gestor = self.kwargs["gestor_id"]
            queryset = Paciente.objects.filter(gestor__id=id_gestor)

            # Verificar si se proporcionó un parámetro de búsqueda
            query_param = self.request.query_params.get("termino", None)
            if query_param:
                queryset = Paciente.buscar_pacientes(query_param).filter(
                    gestor__id=id_gestor
                )

            return queryset
        except KeyError:
            return Paciente.objects.none()
