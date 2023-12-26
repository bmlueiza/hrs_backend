from rest_framework import serializers
from hrsapp.models.observacion import Observacion
from hrsapp.models.paciente import Paciente


class ObservacionSerializer(serializers.ModelSerializer):
    paciente = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),
        required=True,
    )

    class Meta:
        model = Observacion
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Cambia el formato de la fecha de creación a día-mes-año
        representation["fecha_generacion"] = instance.fecha_generacion.strftime(
            "%d-%m-%Y"
        )
        # Reemplaza el ID del gestor con su nombre y apellido
        gestor = instance.gestor
        representation["gestor"] = f"{gestor.first_name} {gestor.last_name}"
        return representation
