from rest_framework import generics
from hrsapp.models.paciente import Paciente
from hrsapp.serializers.paciente_serializer import PacienteSerializer

# CRUD Paciente


# Crear Paciente
class PacienteCreateView(generics.CreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def perform_create(self, serializer):
        gestor_id = self.request.data.get("gestor", None)
        diagnosticos_ids = self.request.data.get("diagnosticos", [])
        paciente = serializer.save()
        paciente.diagnosticos.set(diagnosticos_ids)

        if gestor_id:
            paciente.gestor = gestor_id
            paciente.save()


# Leer Pacientes
class PacienteListView(generics.ListAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Leer un Paciente en específico
class PacienteDetailView(generics.RetrieveAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Actualizar Paciente
class PacienteUpdateView(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Eliminar Paciente
class PacienteDeleteView(generics.DestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
