from rest_framework import viewsets

from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer


class ProtocoloViewSet(viewsets.ModelViewSet):
    queryset = Protocolo.objects.all()
    serializer_class = ProtocoloSerializer
