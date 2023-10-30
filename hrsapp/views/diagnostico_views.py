from rest_framework import generics
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.serializers.diagnostico_serializer import DiagnosticoSerializer

# CRUD Diagnostico


# Crear Diagnostico
class DiagnosticoCreateView(generics.CreateAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer


# Leer Diagnosticos
class DiagnosticoListView(generics.ListAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer


# Leer un Diagnostico en específico
class DiagnosticoDetailView(generics.RetrieveAPIView):
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
