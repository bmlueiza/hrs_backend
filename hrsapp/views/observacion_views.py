from rest_framework import generics
from hrsapp.models.observacion import Observacion
from hrsapp.serializers.observacion_serializer import ObservacionSerializer

# CRUD Observacion


# Crear una Observacion
class ObservacionCreateView(generics.CreateAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer


# Leer Observaciones
class ObservacionListView(generics.ListAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer


# Leer una Observacion en específico
class ObservacionDetailView(generics.RetrieveAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer


# Actualizar una Observacion
class ObservacionUpdateView(generics.UpdateAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer


# Eliminar una Observacion
class ObservacionDeleteView(generics.DestroyAPIView):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer
