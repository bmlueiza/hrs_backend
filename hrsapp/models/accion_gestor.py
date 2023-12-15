from django.db import models


class AccionGestor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def buscar_acciones(cls, query):
        return cls.objects.filter(models.Q(nombre__icontains=query))
