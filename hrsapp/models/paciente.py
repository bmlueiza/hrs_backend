from django.db import models
from .gestor import Gestor
from .diagnostico import Diagnostico
from .medicamento import Medicamento


class Paciente(models.Model):
    rut = models.CharField(max_length=12)
    nombres = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=2)
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=50)
    alergias = models.CharField(max_length=50, null=True)

    # Foreign Keys
    gestor = models.ForeignKey(
        Gestor, on_delete=models.CASCADE, related_name="pacientes"
    )
    diagnosticos = models.ManyToManyField(Diagnostico)
    # motivo_consulta = models.CharField(max_length=50)
    # fecha_ingreso = models.DateField()
    # fecha_alta = models.DateField()

    def __str__(self):
        return self.nombres + " " + self.apellido1
