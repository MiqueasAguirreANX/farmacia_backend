from rest_framework import serializers
from colaboradores.serializers import ColaboradorSerializer
from observaciones.serializers import ObservacionSerializer

from protocolos.models import Protocolo
from clientes.serializers import ClienteSerializer
from servicios.serializers import ServicioSerializer


class ShowProtocoloSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)
    observaciones = ObservacionSerializer(many=True, read_only=True)
    colaborador = ColaboradorSerializer(read_only=True)
    fecha_vencimento = serializers.DateField(read_only=True, input_formats=["%d/%m/%Y"], allow_null=True)

    class Meta:
        model = Protocolo
        fields = "__all__"


class ProtocoloSerializer(serializers.ModelSerializer):
    fecha_vencimento = serializers.DateField(input_formats=["%d/%m/%Y"], allow_null=True)
    
    class Meta:
        model = Protocolo
        fields = "__all__"
