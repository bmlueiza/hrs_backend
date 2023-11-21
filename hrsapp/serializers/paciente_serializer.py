from rest_framework import serializers
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor


class PacienteSerializer(serializers.ModelSerializer):
    gestor = serializers.PrimaryKeyRelatedField(
        queryset=Gestor.objects.all(),  # Asegúrate de importar Gestor
        required=True,
    )

    class Meta:
        model = Paciente
        fields = "__all__"

    def to_representation(self, instance):
        data = super(PacienteSerializer, self).to_representation(instance)
        # Reemplaza los IDs de diagnósticos con los códigos correspondientes
        diagnosticos = instance.diagnosticos.all()
        data["diagnosticos"] = [diagnosticos.codigo for diagnosticos in diagnosticos]
        return data
