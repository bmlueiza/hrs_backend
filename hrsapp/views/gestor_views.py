from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import serializers
from django.contrib.auth import authenticate
from hrsapp.models.gestor import Gestor
from hrsapp.serializers.gestor_serializer import GestorSerializer
from django.contrib.auth import get_user_model

# CRUD Gestor


# Crear y leer Gestores
class GestorCreateListView(generics.ListCreateAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Establece la contraseña utilizando el método set_password
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        gestor = serializer.save()
        gestor.set_password(self.request.data["password"])
        gestor.save()

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
        if gestor.is_superuser:
            return Response(
                {"detail": "No se puede eliminar un gestor administrador"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(gestor)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Obtener gestor según su username
class GestorUsernameView(generics.RetrieveAPIView):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

    def get_object(self):
        username = self.kwargs["username"]
        return Gestor.objects.get(username=username)
