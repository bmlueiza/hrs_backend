from django.db import models
from .paciente import Paciente
from .medicamento import Medicamento
from .medico import Medico


class AsignacionMedicamento(models.Model):
    fecha_asignacion = models.DateField()
    dosis = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)
    estado = models.BooleanField()
    ultimo_retiro = models.DateField()

    # Foreign Keys
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_paciente.nombre + " - " + self.id_medicamento.nombre
