from rest_framework import serializers
from hrsapp.models.observacion import Observacion


class ObservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacion
        fields = "__all__"
