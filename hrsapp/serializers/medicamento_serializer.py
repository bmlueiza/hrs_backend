from rest_framework import serializers
from hrsapp.models.medicamento import Medicamento


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = "__all__"
