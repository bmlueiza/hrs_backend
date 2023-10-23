from rest_framework import serializers
from models.gestor import Gestor


class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        fields = "__all__"
