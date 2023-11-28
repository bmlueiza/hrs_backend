from rest_framework import serializers
from hrsapp.models.historial_medicamento import HistorialMedicamento


class HistorialMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMedicamento
        fields = "__all__"

    def create(self, validated_data):
        historial_medicamento = HistorialMedicamento.objects.create(**validated_data)
        return historial_medicamento
