from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pytz
from clientes.models import Cliente
from colaboradores.models import Colaborador
from farmacias.models import Farmacia
from observaciones.models import Observacion
from protocolos.models import Protocolo
from protocolos.serializers import ProtocoloSerializer, ShowProtocoloSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Avg, Sum, Count


class ObservacionesOfProtocolo(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

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
            "id": x.id,
            "colaborador": x.colaborador.nombre,
            "fecha": x.fecha.astimezone(pytz.timezone("America/Argentina/Buenos_Aires")).strftime("%H:%M %d/%m/%Y"),
            "detalle": x.detalle,
        } for x in protocolo.observaciones.all()]

        return Response(observaciones, status=200)


class MatchedItems(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

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
                data=ShowProtocoloSerializer(protocolo, many=True).data, 
                status=200
            )

        else:
            criterios[criterio] = valor
            criterios["farmacia"] = farmacia

            protocolo = Protocolo.objects.filter(**criterios)

            return Response(
                data=ShowProtocoloSerializer(protocolo, many=True).data, 
                status=200
            )



class GetProtocolosAbiertosByDateRange(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request, date_range: str):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()

        protocolos = []
        if date_range == "ayer":
            today = timezone.now()
            from_ = today - timezone.timedelta(days=1)
            protocolos = Protocolo.objects.filter(
                farmacia=farmacia,
                estado="Abierto",
                fecha__range=(from_, today)
            )
        elif date_range == "semana":
            today = timezone.now()
            from_ = today - timezone.timedelta(weeks=1)
            protocolos = Protocolo.objects.filter(
                farmacia=farmacia,
                estado="Abierto",
                fecha__range=(from_, today)
            )
        elif date_range == "mes":
            today = timezone.now()
            from_ = today - timezone.timedelta(weeks=4)
            protocolos = Protocolo.objects.filter(
                farmacia=farmacia,
                estado="Abierto",
                fecha__range=(from_, today)
            )
        elif date_range == "anio":
            today = timezone.now()
            from_ = today - timezone.timedelta(days=365)
            protocolos = Protocolo.objects.filter(
                farmacia=farmacia,
                estado="Abierto",
                fecha__range=(from_, today)
            )

        return Response(
            data=ShowProtocoloSerializer(protocolos, many=True).data, 
            status=200
        )


class AddObservacionesToProtocolo(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

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
    

class RemoveObservacionesToProtocolo(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self, pk, farmacia: Farmacia):
        try:
            return Protocolo.objects.get(farmacia=farmacia, pk=pk)
        except Protocolo.DoesNotExist:
            raise Protocolo

    def post(self, request, pk, obs_pk):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()
        
        protocolo = self.get_object(pk, farmacia)

        obs = Observacion.objects.filter(
            farmacia=farmacia,
            pk=obs_pk
        )
        if not obs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        obs = obs.first()
        protocolo.observaciones.remove(obs)
        protocolo.save()
        obs.delete()
        return Response({}, status=200)


class ColaboradoresGananciaView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()

        data = {}
        for colaborador in Colaborador.objects.filter(farmacia=farmacia):
            dd = Protocolo.objects.filter(
                farmacia=farmacia, 
                colaborador=colaborador
            ).aggregate(colaborador_venta=Sum("costo"))
            data[colaborador.nombre] = dd["colaborador_venta"]

        return Response(data, status=200)


class GananciasMensualesView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()

        data = {
            "Enero": 1,
            "Febrero": 2,
            "Marzo": 3,
            "Abril": 4,
            "Mayo": 5,
            "Junio": 6,
            "Julio": 7,
            "Agosto": 8,
            "Septiembre": 9,
            "Octubre": 10,
            "Noviembre": 11,
            "Diciembre": 12,
        }
        today = timezone.now()
        for mes in data:
            dd = Protocolo.objects.filter(
                farmacia=farmacia, 
                fecha__year=str(today.year),
                fecha__month=str(data[mes])
            ).aggregate(venta=Sum("costo"))
            data[mes] = dd["venta"]

        return Response(data, status=200)


class MaximosCompradoresView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        farmacia = farmacia.first()

        data = {}
        dd = Cliente.objects.filter(
            farmacia=farmacia
        ).exclude(
            nombre__isnull=True, 
            nombre__exact='',
            nombre=''
        ).annotate(
            compras=Count("protocolo")
        ).order_by("-compras")[0:10]

        dd = [x for x in dd if x.nombre != ""]
        for cliente in dd[0:5]:
            if cliente.apellido:
                data[f"{cliente.nombre.upper()} {cliente.apellido.upper()}"] = cliente.compras
            else:
                data[f"{cliente.nombre.upper()} {cliente.dni}"] = cliente.compras
        return Response(data, status=200)
