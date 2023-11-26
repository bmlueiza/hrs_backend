from rest_framework import serializers
from hrsapp.models.gestor import Gestor


class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        fields = "__all__"

    def validate_rut(self, value):
        if not value:
            raise serializers.ValidationError("Debe ingresar un RUT.")
        elif Gestor.objects.filter(rut=value).exists():
            raise serializers.ValidationError("Ya existe un gestor con ese RUT.")
        return value

    def create(self, validated_data):
        gestor = Gestor.objects.create(**validated_data)
        return gestor
