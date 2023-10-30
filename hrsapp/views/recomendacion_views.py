from rest_framework import generics
from hrsapp.models.recomendacion import Recomendacion
from hrsapp.serializers.recomendacion_serializer import RecomendacionSerializer

# CRUD Recomendacion


# Crear Recomendacion
class RecomendacionCreateView(generics.CreateAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer


# Leer Recomendaciones
class RecomendacionListView(generics.ListAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer


# Leer una Recomendacion en específico
class RecomendacionDetailView(generics.RetrieveAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer


# Actualizar una Recomendacion
class RecomendacionUpdateView(generics.UpdateAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer


# Eliminar una Recomendacion
class RecomendacionDeleteView(generics.DestroyAPIView):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer
