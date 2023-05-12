from rest_framework import viewsets
from rest_framework.response import Response

from colaboradores.models import Colaborador
from colaboradores.serializers import ColaboradorSerializer
from farmacias.models import Farmacia


class ColaboradorViewSet(viewsets.ModelViewSet):
    serializer_class = ColaboradorSerializer

    def get_queryset(self):
        farmacia = Farmacia.objects.filter(user=self.request.user)
        if not farmacia.exists():
            return []
        
        farmacia = farmacia.first()
        return Colaborador.objects.filter(farmacia=farmacia)

    def create(self, request):
        data = request.data
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response(data={}, status=400)
        
        farmacia = farmacia.first()
        data["farmacia"] = farmacia.pk
        
        serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=201, headers=headers
        )
