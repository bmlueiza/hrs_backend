from rest_framework import generics
from hrsapp.models.accion_gestor import AccionGestor
from hrsapp.serializers.accion_gestor_serializer import (
    AccionGestorSerializer,
)

# CRUD AccionGestor


# Crear y leer Acciones de Gestor
class AccionGestorCreateListView(generics.ListCreateAPIView):
    queryset = AccionGestor.objects.all()
    serializer_class = AccionGestorSerializer


# Leer, editar y eliminar una AccionGestor en específico
class AccionGestorDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccionGestor.objects.all()
    serializer_class = AccionGestorSerializer
