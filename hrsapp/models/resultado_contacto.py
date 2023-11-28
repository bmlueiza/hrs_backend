from django.db import models


class ResultadoContacto(models.Model):
    codigo = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
