from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clientes.serializers import ClienteSerializer
from colaboradores.serializers import ColaboradorSerializer
from observaciones.serializers import ObservacionSerializer

from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer
from servicios.serializers import ServicioSerializer


class GetProtocoloByObservacionWord(APIView):

    def post(self, request, *args, **kwargs):
        word = request.data.get("word")
        protocolos = Protocolo.objects.filter(observaciones__detalle__contains=word).distinct()
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
