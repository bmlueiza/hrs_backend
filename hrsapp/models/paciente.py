from django.db import models
from .gestor import Gestor
from .diagnostico import Diagnostico


class Paciente(models.Model):
    SEXO_CHOICES = [
        (0, "No especificado"),
        (1, "Masculino"),
        (2, "Femenino"),
    ]
    RIESGO_CHOICES = [
        (1, "Bajo"),
        (2, "Medio"),
        (3, "Alto"),
    ]

    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=25)
    apellido2 = models.CharField(max_length=25)
    fecha_nacimiento = models.DateField()
    sexo = models.IntegerField(choices=SEXO_CHOICES)
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=50)
    riesgo = models.IntegerField(choices=RIESGO_CHOICES)

    # Foreign Keys
    gestor = models.ForeignKey(
        Gestor, on_delete=models.SET_DEFAULT, default=1, related_name="pacientes"
    )
    diagnosticos = models.ManyToManyField(Diagnostico, related_name="pacientes")

    def __str__(self):
        return self.nombres + " " + self.apellido1 + " " + self.apellido2

    @classmethod
    def buscar_pacientes(cls, query):
        return cls.objects.filter(
            models.Q(nombres__icontains=query)
            | models.Q(apellido1__icontains=query)
            | models.Q(apellido2__icontains=query)
            | models.Q(rut__icontains=query)
        )

    @classmethod
    def get_sex_choices(cls):
        return dict(cls.SEXO_CHOICES)

    @classmethod
    def get_riesgo_choices(cls):
        return dict(cls.RIESGO_CHOICES)
