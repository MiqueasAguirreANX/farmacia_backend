from django.db import models


class Observacion(models.Model):
    colaborador = models.ForeignKey("colaboradores.Colaborador", on_delete=models.CASCADE)
    detalle = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def get_fecha(self):
        return self.fecha.strftime("%H:%M %d/%m/%Y")
