from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from hrsapp.models.gestor import Gestor


class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        exclude = ("password", "is_staff", "date_joined", "last_login")
