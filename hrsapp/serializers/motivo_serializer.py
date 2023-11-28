from rest_framework import serializers
from hrsapp.models.motivo import Motivo


class MotivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivo
        fields = "__all__"
