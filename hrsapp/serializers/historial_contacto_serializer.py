from rest_framework import serializers
from hrsapp.models.historial_contacto import HistorialContacto


class HistorialContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialContacto
        fields = "__all__"

    def to_representation(self, instance):
        representacion = super().to_representation(instance)
        # Cambia el formato de la fecha a día-mes-año
        representacion["fecha"] = instance.fecha.strftime("%d-%m-%Y")
        # Cambia el formato de la hora a hora:minuto
        representacion["hora"] = instance.hora.strftime("%H:%M")
        # Convierte el valor numérico de tipo_motivo a su representación legible
        representacion["tipo_motivo"] = dict(HistorialContacto.TIPO_MOTIVO_CHOICES).get(
            representacion["tipo_motivo"]
        )
        # Remplaza los IDs de las acciones del gestor con sus nombres
        accion_gestor = instance.accion_gestor
        representacion["accion_gestor"] = accion_gestor.nombre
        # Convierte el valor numérico de resultado_contacto a su representación legible
        representacion["resultado_contacto"] = dict(
            HistorialContacto.RESULTADO_CONTACTO_CHOICES
        ).get(representacion["resultado_contacto"])
        return representacion
