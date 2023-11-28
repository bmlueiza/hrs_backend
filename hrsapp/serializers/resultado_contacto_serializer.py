from rest_framework import serializers
from hrsapp.models.resultado_contacto import ResultadoContacto


class ResultadoContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoContacto
        fields = "__all__"

    def create(self, validated_data):
        resultado_contacto = ResultadoContacto.objects.create(**validated_data)
        return resultado_contacto
