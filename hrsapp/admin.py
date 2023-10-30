from django.contrib import admin

# Register your models here.
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.models.medicamento import Medicamento
from hrsapp.models.seguimiento_paciente import SeguimientoPaciente
from hrsapp.models.recomendacion import Recomendacion
from hrsapp.models.observacion import Observacion
from hrsapp.models.medico import Medico
from hrsapp.models.control import Control
from hrsapp.models.asignacion_medicamento import AsignacionMedicamento

admin.site.register(Paciente)
admin.site.register(Gestor)
admin.site.register(Diagnostico)
admin.site.register(Medicamento)
admin.site.register(SeguimientoPaciente)
admin.site.register(Recomendacion)
admin.site.register(Observacion)
admin.site.register(Medico)
admin.site.register(Control)
admin.site.register(AsignacionMedicamento)
