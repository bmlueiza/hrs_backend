from django.db import models


class ActividadMedica(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def buscar_actividades(cls, query):
        return cls.objects.filter(models.Q(nombre__icontains=query))
