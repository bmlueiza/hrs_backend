from rest_framework import serializers
from hrsapp.models.historial_contacto import HistorialContacto


class HistorialContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialContacto
        fields = "__all__"
