from django.db import models
from .paciente import Paciente
from .accion_gestor import AccionGestor
from .motivo import Motivo


class Recomendacion(models.Model):
    fecha = models.DateField()

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="recomendaciones"
    )
    accion_gestor = models.ForeignKey(
        AccionGestor, on_delete=models.CASCADE, related_name="recomendaciones"
    )
    motivo = models.ForeignKey(
        Motivo, on_delete=models.CASCADE, related_name="recomendaciones"
    )
