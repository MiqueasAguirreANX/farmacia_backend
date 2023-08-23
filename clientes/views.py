from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from clientes.models import Cliente
from clientes.serializers import ClienteSerializer
from farmacias.models import Farmacia
from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer, ShowProtocoloSerializer
from rest_framework.authentication import TokenAuthentication


class GetClienteByNombre(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request, nombre, apellido):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        cliente = Cliente.objects.filter(farmacia=farmacia, nombre=nombre, apellido=apellido)
        print(cliente)
        if cliente.exists():
            cliente = cliente.first()
            protocolos = cliente.protocolo_set.all()
            return Response({
                "cliente": ClienteSerializer(cliente).data,
                "protocolos": ProtocoloSerializer(protocolos, many=True).data,
            }, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_404_NOT_FOUND)
    


class GetClienteByDNI(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request, dni):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        cliente = Cliente.objects.filter(farmacia=farmacia, dni=dni)
        print(cliente)
        if cliente.exists():
            cliente = cliente.first()
            protocolos = cliente.protocolo_set.all()
            return Response({
                "cliente": ClienteSerializer(cliente).data,
                "protocolos": ProtocoloSerializer(protocolos, many=True).data,
            }, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_404_NOT_FOUND)


class GetProtocolosDeCliente(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request, cliente: int):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()

        clienteI = get_object_or_404(Cliente, pk=cliente)
        protocolos = Protocolo.objects.filter(cliente=clienteI)
        return Response(
            data=ShowProtocoloSerializer(protocolos, many=True).data, 
            status=200
        )
