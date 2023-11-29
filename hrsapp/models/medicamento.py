from django.db import models


class Medicamento(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def buscar_medicamentos(cls, query):
        return cls.objects.filter(
            models.Q(nombre__icontains=query) | models.Q(codigo__icontains=query)
        )
