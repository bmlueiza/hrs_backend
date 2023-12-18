from rest_framework import serializers
from hrsapp.models.historial_medicamento import HistorialMedicamento


class HistorialMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMedicamento
        fields = "__all__"

    def to_representation(self, instance):
        representacion = super().to_representation(instance)
        # Cambia el formato de la fecha a día-mes-año
        representacion["fecha_inicio"] = instance.fecha_inicio.strftime("%d-%m-%Y")
        representacion["fecha_termino"] = instance.fecha_termino.strftime("%d-%m-%Y")
        representacion["proximo_despacho"] = instance.proximo_despacho.strftime(
            "%d-%m-%Y"
        )
        # Convierte el valor numérico de estado a su representación legible
        representacion["estado"] = dict(HistorialMedicamento.ESTADO_CHOICES).get(
            representacion["estado"]
        )
        # Remplaza los IDs de los pacientes con sus nombres
        paciente = instance.paciente
        representacion["paciente"] = (
            paciente.nombres + " " + paciente.apellido1 + " " + paciente.apellido2
        )
        # Remplaza los IDs de los medicamentos con sus nombres
        medicamento = instance.medicamento
        representacion["medicamento"] = medicamento.nombre
        # Remplaza los IDs de los médicos con sus nombres
        medico = instance.medico
        representacion["medico"] = medico.nombre + " " + medico.apellido
        # Remplaza los IDs de los diagnósticos con sus nombres
        diagnostico = instance.diagnostico
        representacion["diagnostico"] = diagnostico.codigo
        return representacion

    def create(self, validated_data):
        historial_medicamento = HistorialMedicamento.objects.create(**validated_data)
        return historial_medicamento
