from rest_framework import serializers
from hrsapp.models.medico import Medico


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Reemplaza el ID de la especialidad con su nombre
        especialidad = instance.especialidad
        representation["especialidad"] = especialidad.nombre
        return representation
