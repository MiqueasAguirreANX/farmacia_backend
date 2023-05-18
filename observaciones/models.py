from django.db import models
from farmacias.models import Farmacia


class Observacion(models.Model):
    colaborador = models.ForeignKey("colaboradores.Colaborador", null=True, on_delete=models.CASCADE)
    detalle = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)

    def get_fecha(self):
        return self.fecha.strftime("%H:%M %d/%m/%Y")
