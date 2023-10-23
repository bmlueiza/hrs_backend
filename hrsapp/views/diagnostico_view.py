from rest_framework import generics
from models.diagnostico import Diagnostico
from serializers.diagnostico_serializer import DiagnosticoSerializer

# CRUD Diagnostico


# Crear
class CrearDiagnosticos(generics.CreateAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer


# Leer
class ListaDiagnosticos(generics.ListAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer


# Actualizar
class DiagnosticoUpdateView(generics.UpdateAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer


# Eliminar
class DiagnosticoDeleteView(generics.DestroyAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
