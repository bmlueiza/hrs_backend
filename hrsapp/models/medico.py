from django.db import models


class Medico(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    especialidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + " " + self.apellido

    @classmethod
    def buscar_medicos(cls, query):
        return cls.objects.filter(
            models.Q(nombre__icontains=query)
            | models.Q(apellido__icontains=query)
            | models.Q(rut__icontains=query)
            | models.Q(especialidad__icontains=query)
        )

    @classmethod
    def buscar_medicos_especialidad(cls, query):
        return cls.objects.filter(models.Q(especialidad__icontains=query))
