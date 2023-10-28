from django.db import models


class Gestor(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=12)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre + " " + self.apellido
