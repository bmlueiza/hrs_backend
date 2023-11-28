from rest_framework import generics
from hrsapp.models.resultado_contacto import ResultadoContacto
from hrsapp.serializers.resultado_contacto_serializer import (
    ResultadoContactoSerializer,
)


# CRUD ResultadoContacto


# Crear y leer Resultados de Contacto
class ResultadoContactoCreateListView(generics.ListCreateAPIView):
    queryset = ResultadoContacto.objects.all()
    serializer_class = ResultadoContactoSerializer


# Leer, editar y eliminar un ResultadoContacto en específico
class ResultadoContactoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResultadoContacto.objects.all()
    serializer_class = ResultadoContactoSerializer
