from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Colaborador
from .serializers import ColaboradorSerializer
from farmacias.models import Farmacia
from rest_framework.authentication import TokenAuthentication


class CheckEmpleadoCodigo(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request, codigo: str):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        cola = Colaborador.objects.filter(codigo=codigo, farmacia=farmacia)
        if not cola.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        cola = cola.first()
        return Response(ColaboradorSerializer(cola).data, status=status.HTTP_200_OK)