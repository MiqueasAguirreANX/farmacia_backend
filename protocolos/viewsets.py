from rest_framework import viewsets
from rest_framework.response import Response

from farmacias.models import Farmacia

from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer


class ProtocoloViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocoloSerializer

    def get_queryset(self):
        farmacia = Farmacia.objects.filter(user=self.request.user)
        if not farmacia.exists():
            return []
        
        farmacia = farmacia.first()
        cantidad = 500
        get_cantidad = self.request.GET.get("cantidad", False)
        if get_cantidad:
            cantidad = int(get_cantidad)
            if cantidad == -1:
                return Protocolo.objects.filter(farmacia=farmacia)        
            
        return Protocolo.objects.filter(farmacia=farmacia)[:cantidad]

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