from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import serializers
from hrsapp.models.gestor import Gestor
from hrsapp.serializers.gestor_serializer import GestorSerializer

# CRUD Gestor


# Crear Gestor
class GestorCreateView(generics.CreateAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            gestor = serializer.save()
        except serializers.ValidationError as error:
            return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Gestor creado correctamente."}, status=status.HTTP_201_CREATED
        )


# Leer Gestores
class GestorListView(generics.ListAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

    def get_queryset(self):
        termino = self.request.query_params.get("termino", None)
        if termino:
            return Gestor.buscar_gestores(termino)
        return super().get_queryset()


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
