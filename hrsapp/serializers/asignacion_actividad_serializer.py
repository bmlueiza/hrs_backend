from rest_framework import serializers
from hrsapp.models.asignacion_actividad import AsignacionActividad


class AsignacionActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionActividad
        fields = "__all__"
