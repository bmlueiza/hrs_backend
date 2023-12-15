from django.db import models
from .paciente import Paciente
from .gestor import Gestor


class Observacion(models.Model):
    contenido = models.CharField(max_length=250)
    fecha_generacion = models.DateField()

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="observaciones"
    )
    gestor = models.ForeignKey(
        Gestor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="observaciones",
    )
