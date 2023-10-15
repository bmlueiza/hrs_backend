from django.db import models


class Diagnostico(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
