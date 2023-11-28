from django.db import models
from .paciente import Paciente
from .medico import Medico
from .actividad_medica import ActividadMedica


class AsignacionActividad(models.Model):
    ESTADO_CHOICES = [
        (1, "Asignada"),
        (2, "Realizada"),
        (3, "Cancelada"),
    ]
    fecha_asignacion = models.DateField()
    fecha_realizacion = models.DateField()
    estado = models.IntegerField(choices=ESTADO_CHOICES)

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="asignaciones_medicas"
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="asignaciones_medicas",
        blank=True,
        null=True,
    )
    actividad_medica = models.ForeignKey(
        ActividadMedica, on_delete=models.CASCADE, related_name="asignaciones_medicas"
    )
