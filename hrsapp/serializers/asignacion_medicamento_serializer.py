from rest_framework import serializers
from hrsapp.models.asignacion_medicamento import AsignacionMedicamento


class AsignacionMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionMedicamento
        fields = "__all__"
