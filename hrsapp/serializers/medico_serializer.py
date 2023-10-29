from rest_framework import serializers
from hrsapp.models.medico import Medico


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = "__all__"
