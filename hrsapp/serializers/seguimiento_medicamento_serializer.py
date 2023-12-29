from rest_framework import serializers
from hrsapp.models.seguimiento_medicamento import SeguimientoMedicamento


class SeguimientoMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientoMedicamento
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
        representacion["estado"] = dict(SeguimientoMedicamento.ESTADO_CHOICES).get(
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
        # Remplaza los IDs de los diagnósticos con sus nombres
        diagnostico = instance.diagnostico
        representacion["diagnostico"] = (
            diagnostico.codigo if diagnostico is not None else None
        )
        # Remplaza los IDs de los médicos con sus nombres
        medico = instance.medico
        representacion["medico"] = (
            medico.nombre + " " + medico.apellido if medico is not None else None
        )
        return representacion

    def create(self, validated_data):
        seguimiento_medicamento = SeguimientoMedicamento.objects.create(
            **validated_data
        )
        return seguimiento_medicamento
