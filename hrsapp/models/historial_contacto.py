from django.db import models
from .paciente import Paciente
from .accion_gestor import AccionGestor
from .gestor import Gestor


class HistorialContacto(models.Model):
    TIPO_MOTIVO_CHOICES = [
        (1, "Asignación"),
        (2, "Medicamento"),
        (3, "Diagnóstico"),
        (4, "Otro"),
    ]
    RESULTADO_CONTACTO_CHOICES = [
        (1, "Exitoso"),
        (2, "Llamar más tarde"),
        (3, "No contesta"),
        (5, "Rechaza atención"),
        (6, "Número equivocado"),
        (7, "No existe"),
        (8, "Otro"),
    ]

    fecha = models.DateField()
    hora = models.TimeField()
    tipo_motivo = models.IntegerField(choices=TIPO_MOTIVO_CHOICES)
    motivo = models.CharField(max_length=50, blank=True, null=True)
    resultado_contacto = models.IntegerField(choices=RESULTADO_CONTACTO_CHOICES)

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="historial_contacto"
    )
    accion_gestor = models.ForeignKey(
        AccionGestor, on_delete=models.CASCADE, related_name="historial_contacto"
    )
    gestor = models.ForeignKey(
        Gestor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_contacto",
    )
