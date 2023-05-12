from rest_framework import serializers

from farmacias.models import Farmacia


class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = "__all__"