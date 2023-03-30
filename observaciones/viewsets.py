from rest_framework import viewsets

from observaciones.models import Observacion
from observaciones.serializers import ObservacionSerializer


class ObservacionViewSet(viewsets.ModelViewSet):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer

