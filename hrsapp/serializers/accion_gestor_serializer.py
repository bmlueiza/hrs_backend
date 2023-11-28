from rest_framework import serializers
from hrsapp.models.accion_gestor import AccionGestor


class AccionGestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionGestor
        fields = "__all__"

    def create(self, validated_data):
        accion_gestor = AccionGestor.objects.create(**validated_data)
        return accion_gestor
