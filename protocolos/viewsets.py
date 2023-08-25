from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from farmacias.models import Farmacia
from rest_framework.authentication import TokenAuthentication
from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer, ShowProtocoloSerializer
from django.shortcuts import get_object_or_404

class ProtocoloViewSet(viewsets.ModelViewSet):
    serializer_class = ShowProtocoloSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_queryset(self):
        farmacia = Farmacia.objects.filter(user=self.request.user.pk)
        if not farmacia.exists():
            return []
        
        farmacia = farmacia.first()
        try: 
            cantidad = int(self.request.GET.get("cantidad", 500))
        except TypeError:
            cantidad = 500
            
        protocolos = Protocolo.objects.select_related("cliente", "servicio", "colaborador").prefetch_related("observaciones").filter(farmacia=farmacia)
        if cantidad == -1:
            return protocolos
        
        if protocolos.count() < cantidad:
            return protocolos
        
        return protocolos[:cantidad]

    def create(self, request):
        data = request.data
        farmacia = Farmacia.objects.filter(user=request.user.pk)
        if not farmacia.exists():
            return Response(data={}, status=404)
        
        farmacia = farmacia.first()
        data["farmacia"] = farmacia.pk
        
        serializer = ProtocoloSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        prot = serializer.save()
        headers = self.get_success_headers(serializer.data)
        sprot = ShowProtocoloSerializer(prot)
        return Response(
            sprot.data, status=201, headers=headers
        )
    
    def partial_update(self, request, pk=None):
        data = request.data
        farmacia = Farmacia.objects.filter(user=request.user.pk)
        if not farmacia.exists():
            return Response(data={}, status=404)
        
        farmacia = farmacia.first()
        data["farmacia"] = farmacia.pk
        
        protocolo = Protocolo.objects.filter(pk=pk, farmacia=farmacia)
        if not protocolo.exists():
            return Response(data={}, status=404)
        
        protocolo = protocolo.first()
        serializer = ProtocoloSerializer(instance=protocolo, data=data)
        serializer.is_valid(raise_exception=True)
        prot = serializer.save()
        headers = self.get_success_headers(serializer.data)
        sprot = ShowProtocoloSerializer(prot)
        return Response(
            sprot.data, status=200, headers=headers
        )