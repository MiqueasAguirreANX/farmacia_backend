from django.db import models
from farmacias.models import Farmacia


class Colaborador(models.Model):
    nombre = models.CharField(max_length=250)
    apellido = models.CharField(max_length=250, blank=True, null=True)
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=(
        ("ADMIN", "ADMIN"),
        ("COLABORADOR", "COLABORADOR"),
        ("LECTURA", "LECTURA"),
    ), default="LECTURA")
    codigo = models.CharField(max_length=3)

    def get_colaborador_observaciones(self):
        """Retorna las observaciones del colaborador"""
        return self.observacion_set.all()
    
    def get_colaborador_protocolos(self):
        """Retorna los protocolos del colaborador"""
        return self.observacion_set.all()


    def __str__(self):
        return f"{self.nombre} - {self.farmacia.nombre}"
    