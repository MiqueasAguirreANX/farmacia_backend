from rest_framework import serializers

from clientes.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    dni = serializers.IntegerField(
        min_value=1000000
    )

    class Meta:
        model = Cliente
        fields = "__all__"
