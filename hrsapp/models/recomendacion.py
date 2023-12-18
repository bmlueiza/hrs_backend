from django.db import models
from .paciente import Paciente
from .accion_gestor import AccionGestor
from .motivo import Motivo


class Recomendacion(models.Model):
    TIPO_MOTIVO_CHOICES = [
        (1, "Asignación"),
        (2, "Medicamento"),
        (3, "Diagnóstico"),
        (4, "Otro"),
    ]
    fecha = models.DateField()
    tipo_motivo = models.IntegerField(choices=TIPO_MOTIVO_CHOICES)
    motivo = models.CharField(max_length=50)

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="recomendaciones"
    )
    accion_gestor = models.ForeignKey(
        AccionGestor, on_delete=models.CASCADE, related_name="recomendaciones"
    )
