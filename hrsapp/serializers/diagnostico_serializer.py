from rest_framework import serializers
from hrsapp.models.diagnostico import Diagnostico


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = "__all__"

    def validate_codigo(self, value):
        if value == "":
            raise serializers.ValidationError("Debe ingresar un código.")
        elif Diagnostico.objects.filter(codigo=value).exists():
            raise serializers.ValidationError(
                "Ya existe un diagnóstico con ese código."
            )
        return value

    def create(self, validated_data):
        diagnostico = Diagnostico.objects.create(**validated_data)
        return diagnostico
