from rest_framework import generics
from hrsapp.models.control import Control
from hrsapp.serializers.control_serializer import ControlSerializer

# CRUD Control


# Crear Control
class ControlCreateView(generics.CreateAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer


# Leer Controles
class ControlListView(generics.ListAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer


# Leer un Control en específico
class ControlDetailView(generics.RetrieveAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer


# Actualizar Control
class ControlUpdateView(generics.UpdateAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer


# Eliminar Control
class ControlDeleteView(generics.DestroyAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
