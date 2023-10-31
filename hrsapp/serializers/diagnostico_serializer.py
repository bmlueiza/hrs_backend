from rest_framework import serializers
from hrsapp.models.diagnostico import Diagnostico


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = "__all__"


class DiagnosticoCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ["codigo"]
