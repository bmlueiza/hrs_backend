from rest_framework import serializers
from hrsapp.models.recomendacion import Recomendacion


class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = "__all__"
