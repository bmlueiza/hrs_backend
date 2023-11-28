from rest_framework import generics
from hrsapp.models.recomendacion import Recomendacion
from hrsapp.serializers.recomendacion_serializer import RecomendacionSerializer

# CRUD Recomendacion


# Crear y leer Recomendaciones
class RecomendacionListView(generics.ListCreateAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer


# Leer, editar y eliminar una Recomendacion en específico
class RecomendacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer
