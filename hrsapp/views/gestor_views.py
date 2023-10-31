from rest_framework import generics
from hrsapp.models.gestor import Gestor
from hrsapp.serializers.gestor_serializer import GestorSerializer

# CRUD Gestor


# Crear Gestor
class GestorCreateView(generics.CreateAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Leer Gestores
class GestorListView(generics.ListAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Leer un Gestor en específico
class GestorDetailView(generics.RetrieveAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Actualizar Gestor
class GestorUpdateView(generics.UpdateAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


# Eliminar Gestor
class GestorDeleteView(generics.DestroyAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer
