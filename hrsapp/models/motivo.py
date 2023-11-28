from django.db import models


class Motivo(models.Model):
    TIPO_CHOICES = [
        (1, "Actividad médica"),
        (2, "Medicamento"),
        (3, "Diagnóstico"),
    ]
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.PositiveIntegerField(choices=TIPO_CHOICES)

    def __str__(self):
        return self.nombre
