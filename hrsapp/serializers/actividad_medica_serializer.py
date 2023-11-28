from rest_framework import serializers
from hrsapp.models.actividad_medica import ActividadMedica


class ActividadMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadMedica
        fields = "__all__"
