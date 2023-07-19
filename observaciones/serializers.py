from rest_framework import serializers
import pytz
from observaciones.models import Observacion


class ObservacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Observacion
        fields = "__all__"
