from rest_framework import viewsets

from colaboradores.models import Colaborador
from colaboradores.serializers import ColaboradorSerializer


class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

