from rest_framework import viewsets

from servicios.models import Servicio
from servicios.serializers import ServicioSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
