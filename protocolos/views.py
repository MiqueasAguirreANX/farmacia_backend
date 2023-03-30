from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from colaboradores.models import Colaborador
from observaciones.models import Observacion
from protocolos.models import Protocolo


class ObservacionesOfProtocolo(APIView):

    def get_object(self, pk):
        try:
            return Protocolo.objects.get(pk=pk)
        except Protocolo.DoesNotExist:
            raise Protocolo

    def get(self, request, pk):
        protocolo = self.get_object(pk)
        observaciones = [{
            "colaborador": x.colaborador.nombre,
            "fecha": x.get_fecha(),
            "detalle": x.detalle,
        } for x in protocolo.observaciones.all()]

        return Response(observaciones, status=200)


class AddObservacionesToProtocolo(APIView):

    def get_object(self, pk):
        try:
            return Protocolo.objects.get(pk=pk)
        except Protocolo.DoesNotExist:
            raise Protocolo

    def post(self, request, pk):
        protocolo = self.get_object(pk)
        col = Colaborador.objects.filter(pk=request.data.get("colaborador"))
        if not col.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        col = col.first()

        obs = Observacion(
            colaborador=col,
            detalle=request.data.get("detalle")
        )
        obs.save()
        protocolo.observaciones.add(obs)
        protocolo.save()
        return Response({}, status=200)
