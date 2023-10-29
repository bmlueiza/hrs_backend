from rest_framework import serializers
from hrsapp.models.paciente import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    # diagnostico = DiagnosticoCodigoSerializer(many=True, read_only=True)

    class Meta:
        model = Paciente
        exclude = ["diagnostico"]

    def to_representation(self, instance):
        data = super(PacienteSerializer, self).to_representation(instance)
        # Reemplaza los IDs de diagnósticos con los códigos correspondientes
        diagnosticos = instance.diagnostico.all()
        data["diagnosticos"] = [diagnosticos.codigo for diagnosticos in diagnosticos]
        return data
