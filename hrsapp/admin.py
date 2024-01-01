from django.contrib import admin

# Register your models here.
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.models.especialidad_medica import EspecialidadMedica
from hrsapp.models.gestor import Gestor
from hrsapp.models.paciente import Paciente
from hrsapp.models.medico import Medico
from hrsapp.models.medicamento import Medicamento
from hrsapp.models.actividad_medica import ActividadMedica
from hrsapp.models.accion_gestor import AccionGestor
from hrsapp.models.historial_contacto import HistorialContacto
from hrsapp.models.observacion import Observacion
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.models.seguimiento_medicamento import SeguimientoMedicamento

admin.site.register(Diagnostico)
admin.site.register(EspecialidadMedica)
admin.site.register(Gestor)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Medicamento)
admin.site.register(ActividadMedica)
admin.site.register(AccionGestor)
admin.site.register(HistorialContacto)
admin.site.register(Observacion)
admin.site.register(AsignacionActividad)
admin.site.register(SeguimientoMedicamento)
