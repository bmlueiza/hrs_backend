from django.db import models
from .paciente import Paciente
from .accion_gestor import AccionGestor
from .resultado_contacto import ResultadoContacto
from .motivo import Motivo


class HistorialContacto(models.Model):
    fecha = models.DateField()

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="historial_contacto"
    )
    accion_gestor = models.ForeignKey(
        AccionGestor, on_delete=models.CASCADE, related_name="historial_contacto"
    )
    resultado_contacto = models.ForeignKey(
        ResultadoContacto, on_delete=models.CASCADE, related_name="historial_contacto"
    )
    gestor = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="hc_gestor"
    )
    motivo = models.ForeignKey(
        Motivo, on_delete=models.CASCADE, related_name="historial_contacto"
    )
