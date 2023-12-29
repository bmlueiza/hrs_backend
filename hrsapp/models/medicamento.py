from django.db import models


class Medicamento(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def buscar_medicamentos(cls, query):
        return cls.objects.filter(
            models.Q(nombre__icontains=query) | models.Q(descripcion__icontains=query)
        )
