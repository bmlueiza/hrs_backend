from rest_framework import serializers
from hrsapp.models.diagnostico import Diagnostico


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ["nombre", "codigo", "descripcion"]


class DiagnosticoCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ["codigo"]
