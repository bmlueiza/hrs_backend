from django.db import models


class Medico(models.Model):
    rut = models.CharField(max_length=11)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + " " + self.apellido
