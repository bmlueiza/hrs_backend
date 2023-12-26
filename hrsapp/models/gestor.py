from django.contrib.auth.models import AbstractUser
from django.db import models


class Gestor(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=12, unique=True)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @classmethod
    def buscar_gestores(cls, query):
        return cls.objects.filter(
            models.Q(first_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(rut__icontains=query)
            | models.Q(username__icontains=query)
        )
