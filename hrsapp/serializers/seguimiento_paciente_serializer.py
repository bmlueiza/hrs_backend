from rest_framework import serializers
from hrsapp.models.seguimiento_paciente import SeguimientoPaciente


class SeguimientoPacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientoPaciente
        fields = "__all__"
