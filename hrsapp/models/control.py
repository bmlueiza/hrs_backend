from django.db import models
from .paciente import Paciente
from .medico import Medico


class Control(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    estado = models.CharField(max_length=20)

    # Foreign Keys
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
