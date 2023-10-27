from django.db import models
from .paciente import Paciente


class Observacion(models.Model):
    contenido = models.CharField(max_length=250)
    fecha = models.DateField()

    # Foreign Keys
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    gestor = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="gestor_id"
    )
