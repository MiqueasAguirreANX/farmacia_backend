from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from clientes.serializers import ClienteSerializer
from colaboradores.serializers import ColaboradorSerializer
from farmacias.models import Farmacia
from observaciones.serializers import ObservacionSerializer

from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer
from servicios.serializers import ServicioSerializer
from rest_framework.authentication import TokenAuthentication

class GetProtocoloByObservacionWord(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def post(self, request, *args, **kwargs):

        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()

        
        word = request.data.get("word")
        protocolos = Protocolo.objects.filter(farmacia=farmacia, observaciones__detalle__contains=word).distinct()
        data = []

        for protocolo in protocolos:
            prot = ProtocoloSerializer(protocolo).data
            observaciones = ObservacionSerializer(protocolo.observaciones, many=True).data
            cliente = ClienteSerializer(protocolo.cliente).data
            colaborador = ColaboradorSerializer(protocolo.colaborador).data
            servicio = ServicioSerializer(protocolo.servicio).data

            data.append({
                "protocolo": prot,
                "observaciones": observaciones,
                "cliente": cliente,
                "colaborador": colaborador,
                "servicio": servicio,
            })
        
        return Response(data={
            "word": word,
            "data": data,
        }, status=status.HTTP_200_OK)
