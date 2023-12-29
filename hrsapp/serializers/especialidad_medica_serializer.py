from rest_framework import serializers
from hrsapp.models.especialidad_medica import EspecialidadMedica


class EspecialidadMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspecialidadMedica
        fields = "__all__"
