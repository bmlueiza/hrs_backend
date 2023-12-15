from rest_framework import serializers
from hrsapp.models.asignacion_actividad import AsignacionActividad


class AsignacionActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionActividad
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Cambia el formato de la fecha de asignación a día-mes-año
        representation["fecha_asignacion"] = instance.fecha_asignacion.strftime(
            "%d-%m-%Y"
        )
        # Cambia el formato de la fecha de realización a día-mes-año
        representation["fecha_actividad"] = instance.fecha_actividad.strftime(
            "%d-%m-%Y"
        )
        # Reemplaza el ID del paciente con su nombre y apellido
        paciente = instance.paciente
        representation["paciente"] = f"{paciente.nombre} {paciente.apellido}"
        # Reemplaza el ID del médico con su nombre y apellido
        medico = instance.medico
        if medico is not None:
            representation["medico"] = f"{medico.nombre} {medico.apellido}"
        # Reemplaza el ID de la actividad médica con su nombre
        actividad_medica = instance.actividad_medica
        representation["actividad_medica"] = actividad_medica.nombre
        # Convertir valores numéricos a sus representaciones legibles
        representation["estado"] = dict(AsignacionActividad.ESTADO_CHOICES).get(
            representation["estado"]
        )
        return representation
