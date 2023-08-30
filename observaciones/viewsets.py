from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from farmacias.models import Farmacia

from observaciones.models import Observacion
from observaciones.serializers import ObservacionSerializer
from rest_framework.authentication import TokenAuthentication

class ObservacionViewSet(viewsets.ModelViewSet):
    serializer_class = ObservacionSerializer
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAdminUser,]
        else:
            permission_classes = [IsAuthenticated,]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        farmacia = Farmacia.objects.filter(user=self.request.user)
        if not farmacia.exists():
            return []
        
        farmacia = farmacia.first()
        return Observacion.objects.filter(farmacia=farmacia)

    def create(self, request):
        data = request.data
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return Response(data={}, status=400)
        
        farmacia = farmacia.first()
        data["farmacia"] = farmacia.pk
        
        serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=201, headers=headers
        )
