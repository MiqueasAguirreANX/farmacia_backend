from django.db import models

from farmacias.models import Farmacia


class Servicio(models.Model):
    nombre = models.CharField(max_length=250)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)

    class Meta:
        ordering = ["nombre"]
