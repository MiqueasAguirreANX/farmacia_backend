from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clientes.models import Cliente
from clientes.serializers import ClienteSerializer
from farmacias.models import Farmacia
from protocolos.serializers import ProtocoloSerializer


class GetClienteByNombre(APIView):

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
