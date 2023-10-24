from rest_framework import generics
from hrsapp.models.gestor import Gestor
from hrsapp.serializers.gestor_serializer import GestorSerializer

# CRUD Gestor


# Crear
class CrearGestors(generics.CreateAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Leer
class ListaGestors(generics.ListAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Actualizar
class GestorUpdateView(generics.UpdateAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Eliminar
class GestorDeleteView(generics.DestroyAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer
