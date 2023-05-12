from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from colaboradores.models import Colaborador
from farmacias.models import Farmacia
from observaciones.models import Observacion
from protocolos.models import Protocolo


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
