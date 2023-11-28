from django.db import models
from .paciente import Paciente
from .medicamento import Medicamento
from .medico import Medico


class HistorialMedicamento(models.Model):
    ESTADO_CHOICES = [
        (1, "Al día"),
        (2, "No retirado"),
        (2, "Terminado"),
        (3, "Suspendido"),
    ]
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    administracion = models.CharField(max_length=150, blank=True, null=True)
    cantd_otorgada = models.CharField(max_length=100, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADO_CHOICES)
    ultimo_retiro = models.DateField(blank=True, null=True)

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="historial_medicamento"
    )
    medicamento = models.ForeignKey(
        Medicamento, on_delete=models.CASCADE, related_name="historial_medicamento"
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="historial_medicamento",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.id_paciente.nombre + " - " + self.id_medicamento.nombre
