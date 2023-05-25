from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from colaboradores.models import Colaborador
from farmacias.models import Farmacia
from observaciones.models import Observacion
from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer


class ObservacionesOfProtocolo(APIView):

    def get_object(self, pk, farmacia: Farmacia):
        try:
            return Protocolo.objects.get(farmacia=farmacia, pk=pk)
        except Protocolo.DoesNotExist:
            raise Protocolo

    def get(self, request, pk):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        
        protocolo = self.get_object(pk, farmacia)
        observaciones = [{
            "colaborador": x.colaborador.nombre,
            "fecha": x.get_fecha(),
            "detalle": x.detalle,
        } for x in protocolo.observaciones.all()]

        return Response(observaciones, status=200)


class MatchedItems(APIView):

    def post(self, request):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        
        criterios = {}
        criterio = request.data.get("criterio")
        valor = request.data.get("valor")

        if criterio == "fecha":
            year = valor.split("/")[2]
            month = valor.split("/")[1]
            day = valor.split("/")[0]

            protocolo = Protocolo.objects.filter(
                farmacia=farmacia,
                fecha__year=year,
                fecha__month=month,
                fecha__day=day,
            )

            return Response(
                data=ProtocoloSerializer(protocolo, many=True).data, 
                status=200
            )

        else:
            criterios[criterio] = valor
            criterios["farmacia"] = farmacia

            protocolo = Protocolo.objects.filter(**criterios)

            return Response(
                data=ProtocoloSerializer(protocolo, many=True).data, 
                status=200
            )


class AddObservacionesToProtocolo(APIView):

    def get_object(self, pk, farmacia: Farmacia):
        try:
            return Protocolo.objects.get(farmacia=farmacia, pk=pk)
        except Protocolo.DoesNotExist:
            raise Protocolo

    def post(self, request, pk):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        
        protocolo = self.get_object(pk, farmacia)
        col = Colaborador.objects.filter(farmacia=farmacia, pk=request.data.get("colaborador"))
        if not col.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        col = col.first()

        obs = Observacion(
            farmacia=farmacia,
            colaborador=col,
            detalle=request.data.get("detalle")
        )
        obs.save()
        protocolo.observaciones.add(obs)
        protocolo.save()
        return Response({}, status=200)
