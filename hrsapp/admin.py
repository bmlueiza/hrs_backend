from django.contrib import admin

# Register your models here.
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico

admin.site.register(Paciente)
admin.site.register(Gestor)
admin.site.register(Diagnostico)
