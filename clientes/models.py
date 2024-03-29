from django.db import models

from farmacias.models import Farmacia


class Cliente(models.Model):
    dni = models.IntegerField(default=0, blank=True, null=True)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    apellido = models.CharField(max_length=250, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    domicilio = models.CharField(max_length=250, blank=True, null=True)
    entre_calles = models.CharField(max_length=250, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"