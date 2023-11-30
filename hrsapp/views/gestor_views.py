from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import serializers
from hrsapp.models.gestor import Gestor
from hrsapp.serializers.gestor_serializer import GestorSerializer

# CRUD Gestor


# Crear y leer Gestores
class GestorCreateListView(generics.ListCreateAPIView):
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

    def get_queryset(self):
        termino = self.request.query_params.get("termino", None)
        if termino:
            return Gestor.buscar_gestores(termino)
        return super().get_queryset()


# Leer, editar y eliminar un Gestor en específico
class GestorDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

    def delete(self, request, *args, **kwargs):
        gestor = self.get_object()
        if gestor.usuario.is_superuser:
            return Response(
                {"detail": "No se puede eliminar un gestor administrador"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(gestor)
        return Response(status=status.HTTP_204_NO_CONTENT)
