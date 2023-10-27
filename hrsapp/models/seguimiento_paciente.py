from django.db import models
from .paciente import Paciente


class SeguimientoPaciente(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)
    resultado = models.CharField(max_length=50)

    # Foreign Keys
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
