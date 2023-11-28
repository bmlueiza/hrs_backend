from django.db import models


class AccionGestor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.PositiveIntegerField(unique=True)
    estado = models.BooleanField(default=True)

    @classmethod
    def buscar_acciones(cls, query):
        return cls.objects.filter(
            models.Q(nombre__icontains=query) | models.Q(codigo__icontains=query)
        )
