from django.db import models
from .gestor import Gestor
from .diagnostico import Diagnostico


class Paciente(models.Model):
    rut = models.CharField(max_length=11)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=2)
    telefono = models.CharField(max_length=11)
    direccion = models.CharField(max_length=50)

    # Foreign Keys
    gestor = models.ForeignKey(Gestor, on_delete=models.CASCADE)
    diagnostico = models.ManyToManyField(Diagnostico)

    # motivo_consulta = models.CharField(max_length=50)
    # fecha_ingreso = models.DateField()
    # fecha_alta = models.DateField()
    # medicacion = models.CharField(max_length=50)
    # observaciones = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + " " + self.apellido1
