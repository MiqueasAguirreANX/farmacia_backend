from rest_framework.response import Response
from rest_framework.views import APIView

from farmacias.models import Farmacia
from farmacias.serializers import FarmaciaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class CurrentFarmacia(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get(self, request):
        farmacia = Farmacia.objects.filter(user=request.user)
        if not farmacia.exists():
            return []
        
        farmacia = farmacia.first()
        return Response(
            data=FarmaciaSerializer(farmacia).data,
            status=200
        )



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })