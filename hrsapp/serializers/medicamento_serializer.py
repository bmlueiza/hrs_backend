from rest_framework import serializers
from hrsapp.models.medicamento import Medicamento


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = "__all__"

    def create(self, validated_data):
        medicamento = Medicamento.objects.create(**validated_data)
        return medicamento
