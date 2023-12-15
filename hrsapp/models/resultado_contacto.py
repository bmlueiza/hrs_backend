from django.db import models


class ResultadoContacto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
