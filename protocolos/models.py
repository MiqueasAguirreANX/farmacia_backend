from django.db import models
from django.utils import timezone
from farmacias.models import Farmacia


class Protocolo(models.Model):
    ESTADO_CHOICES = (
        ("Abierto", "Abierto"),
        ("Suspendido", "Suspendido"),
        ("Cerrado", "Cerrado"),
        ("En Proceso", "En Proceso"),
        ("Presupuesto", "Presupuesto"),
    )

    fecha = models.DateTimeField(auto_now_add=True, editable=True)
    cliente = models.ForeignKey("clientes.Cliente", blank=True, null=True, on_delete=models.CASCADE)
    servicio = models.ForeignKey("servicios.Servicio", blank=True, null=True, on_delete=models.CASCADE)
    observaciones = models.ManyToManyField("observaciones.Observacion")
    costo_proveedor = models.FloatField(default=0, blank=True, null=True)
    deposito = models.FloatField(default=0, blank=True, null=True)
    costo = models.FloatField(default=0, blank=True, null=True)
    senia = models.FloatField(default=0, blank=True, null=True)
    falta_abonar = models.FloatField(default=0, blank=True, null=True)
    pagado = models.BooleanField(default=False, blank=True, null=True)
    delivery = models.BooleanField(default=False, blank=True, null=True)
    colaborador = models.ForeignKey("colaboradores.Colaborador", blank=True, null=True, on_delete=models.CASCADE)
    estado = models.CharField(max_length=40, choices=ESTADO_CHOICES, blank=True, null=True)
    fecha_vencimento = models.DateField(blank=True, null=True)
    entregado_proveedor = models.BooleanField(default=False, blank=True, null=True)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    def get_fecha(self):
        return self.fecha.strftime("%H:%M %d/%m/%Y")
    
    class Meta:
        ordering = ["-fecha"]
