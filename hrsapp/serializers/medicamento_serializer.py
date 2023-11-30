from rest_framework import serializers
from hrsapp.models.medicamento import Medicamento


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = "__all__"

    def validate_codigo(self, value):
        if value == "":
            raise serializers.ValidationError("Debe ingresar un código.")
        elif Medicamento.objects.filter(codigo=value).exists():
            raise serializers.ValidationError(
                "Ya existe un medicamento con ese código."
            )
        return value

    def create(self, validated_data):
        medicamento = Medicamento.objects.create(**validated_data)
        return medicamento
