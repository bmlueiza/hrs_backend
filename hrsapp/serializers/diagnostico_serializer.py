from rest_framework import serializers
from models.diagnostico import Diagnostico


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ["nombre", "codigo", "descripcion"]
