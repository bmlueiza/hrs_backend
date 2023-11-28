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
        representation = super().to_representation(instance)
        # Cambia el formato de la fecha de nacimiento a día-mes-año
        representation["fecha_nacimiento"] = instance.fecha_nacimiento.strftime(
            "%d-%m-%Y"
        )
        # Reemplaza los IDs de diagnósticos con los códigos correspondientes
        diagnosticos = instance.diagnosticos.all()
        representation["diagnosticos"] = [
            diagnostico.codigo for diagnostico in diagnosticos
        ]
        return representation

    def validate_rut(self, value):
        if not value:
            raise serializers.ValidationError("Debe ingresar un RUT.")
        elif Paciente.objects.filter(rut=value).exists():
            raise serializers.ValidationError("Ya existe un paciente con ese RUT.")
        return value

    def create(self, validated_data):
        rut = validated_data.get("rut")

        # Extrae los IDs de diagnósticos de los datos validados
        diagnosticos = validated_data.pop("diagnosticos")
        # Crea el paciente
        paciente = Paciente.objects.create(**validated_data)
        # Asigna los diagnósticos al paciente
        for diagnostico in diagnosticos:
            paciente.diagnosticos.add(diagnostico)
        return paciente
