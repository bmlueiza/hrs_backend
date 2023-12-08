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

    def save(self, *args, **kwargs):
        # Verificar si el gestor está asignado al paciente
        if self.gestor != self.paciente.gestor:
            raise ValueError("El gestor no está asignado al paciente.")

        # Llamada al método save del modelo padre
        super().save(*args, **kwargs)
