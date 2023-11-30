from rest_framework import serializers
from hrsapp.models.observacion import Observacion
from hrsapp.models.paciente import Paciente


class ObservacionSerializer(serializers.ModelSerializer):
    paciente = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),  # Asegúrate de importar Paciente
        required=True,
    )

    class Meta:
        model = Observacion
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Cambia el formato de la fecha de creación a día-mes-año
        representation["fecha_creacion"] = instance.fecha_creacion.strftime("%d-%m-%Y")
        # Reemplaza el ID del paciente con el RUT correspondiente
        paciente = instance.pacientes.all()
        representation["paciente"] = [paciente.rut for paciente in paciente]
        return representation

    def create(self, validated_data):
        rut = validated_data.get("rut")
        paciente = Paciente.objects.get(rut=rut)
        observacion = Observacion.objects.create(**validated_data)
        observacion.paciente.add(paciente)
        return observacion
