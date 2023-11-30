from rest_framework import generics, status
from rest_framework.response import Response
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.serializers.diagnostico_serializer import DiagnosticoSerializer

# CRUD Diagnostico


# Crear y leer Diagnostico
class DiagnosticoCreateListView(generics.ListCreateAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer

    def get_queryset(self):
        termino = self.request.query_params.get("termino", None)
        if termino:
            return Diagnostico.buscar_diagnosticos(termino)
        return super().get_queryset()


# Leer, actualizar y eliminar Diagnostico
class DiagnosticoDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
