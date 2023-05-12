from rest_framework.response import Response
from rest_framework.views import APIView

from farmacias.models import Farmacia
from farmacias.serializers import FarmaciaSerializer


class CurrentFarmacia(APIView):

    def get(self, request):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return []
        
        farmacia = farmacia.first()
        return Response(
            data=FarmaciaSerializer(farmacia).data,
            status=200
        )

