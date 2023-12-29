from django.db import models
from .paciente import Paciente
from .medicamento import Medicamento
from .medico import Medico
from .diagnostico import Diagnostico


class SeguimientoMedicamento(models.Model):
    ESTADO_CHOICES = [
        (1, "Al día"),
        (2, "No retirado"),
        (3, "Terminado"),
        (4, "Suspendido"),
    ]
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    cantd_otorgada = models.CharField(max_length=100, blank=True, null=True)
    indicacion_uso = models.CharField(max_length=150, blank=True, null=True)
    proximo_despacho = models.DateField()
    estado = models.IntegerField(choices=ESTADO_CHOICES)

    # Foreign Keys
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="historial_medicamento"
    )
    medicamento = models.ForeignKey(
        Medicamento, on_delete=models.CASCADE, related_name="historial_medicamento"
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.SET_NULL,
        related_name="historial_medicamento",
        blank=True,
        null=True,
    )
    diagnostico = models.ForeignKey(
        Diagnostico,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="historial_medicamento",
    )

    def __str__(self):
        return (
            self.paciente.nombres
            + " "
            + self.paciente.apellido1
            + " - "
            + self.medicamento.nombre
        )
