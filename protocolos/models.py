from django.db import models
from django.utils import timezone


class Protocolo(models.Model):
    ESTADO_CHOICES = (
        ("Abierto", "Abierto"),
        ("Suspendido", "Suspendido"),
        ("Cerrado", "Cerrado"),
        ("En Proceso", "En Proceso"),
        ("Presupuesto", "Presupuesto"),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey("clientes.Cliente", blank=True, null=True, on_delete=models.CASCADE)
    servicio = models.ForeignKey("servicios.Servicio", blank=True, null=True, on_delete=models.CASCADE)
    observaciones = models.ManyToManyField("observaciones.Observacion")
    costo_proveedor = models.FloatField(default=0)
    deposito = models.FloatField(default=0)
    costo = models.FloatField(default=0)
    senia = models.FloatField(default=0)
    falta_abonar = models.FloatField(default=0)
    pagado = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    colaborador = models.ForeignKey("colaboradores.Colaborador", blank=True, null=True, on_delete=models.CASCADE)
    estado = models.CharField(max_length=40, choices=ESTADO_CHOICES)
    fecha_vencimento = models.DateField(default=timezone.now().date())
    entregado_proveedor = models.BooleanField(default=False)

    def get_fecha(self):
        return self.fecha.strftime("%H:%M %d/%m/%Y")
