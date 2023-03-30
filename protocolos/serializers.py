from rest_framework import serializers

from protocolos.models import Protocolo


class ProtocoloSerializer(serializers.ModelSerializer):

    class Meta:
        model = Protocolo
        fields = "__all__"
