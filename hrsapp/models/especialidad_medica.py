from django.db import models


class EspecialidadMedica(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def buscar_especialidades(cls, query):
        return cls.objects.filter(models.Q(nombre__icontains=query))
