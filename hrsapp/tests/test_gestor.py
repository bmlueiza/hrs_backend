import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.gestor import Gestor

# Modelo


@pytest.mark.django_db
def test_crear_gestor():
    gestor = Gestor.objects.create(
        rut="12.345.678-9",
        first_name="Nuevo",
        last_name="Gestor",
        username="NuevoGestor",
        telefono="987654321",
        email="nuevo@gestor.com",
        password="hash123",
        admin=False,
    )

    assert Gestor.objects.count() == 1
    assert gestor.rut == "12.345.678-9"
    assert gestor.first_name == "Nuevo"
    assert gestor.last_name == "Gestor"
    assert gestor.username == "NuevoGestor"
    assert gestor.telefono == "987654321"
    assert gestor.email == "nuevo@gestor.com"
    assert gestor.password == "hash123"
    assert gestor.admin == False


@pytest.mark.django_db
def test_rut_unico_gestor():
    Gestor.objects.create(
        rut="12.345.678-9",
        first_name="Gestor1",
        last_name="last_name",
        username="NuevoGestor",
        telefono="12.345.678-9",
        email="gestor1@example.com",
        password="hash123",
        admin=False,
    )
    with pytest.raises(IntegrityError):
        Gestor.objects.create(
            rut="12.345.678-9",
            first_name="Gestor2",
            last_name="last_name",
            telefono="987654321",
            email="gestor2@example.com",
            password="hash456",
            admin=False,
        )


@pytest.mark.django_db
def test_buscar_gestores():
    Gestor.objects.create(
        first_name="John",
        last_name="Doe",
        username="john_doe",
        password="testpassword",
        rut="123456789",
        telefono="555-1234",
        admin=True,
    )
    Gestor.objects.create(
        first_name="Jane",
        last_name="Doe",
        username="jane_doe",
        password="testpassword",
        rut="987654321",
        telefono="555-5678",
        admin=False,
    )

    # Buscar por nombre
    result = Gestor.buscar_gestores("John")
    assert result.count() == 1

    # Buscar por apellido
    result = Gestor.buscar_gestores("Doe")
    assert result.count() == 2

    # Buscar por rut
    result = Gestor.buscar_gestores("123456789")
    assert result.count() == 1

    # Buscar por username
    result = Gestor.buscar_gestores("john_doe")
    assert result.count() == 1


# Views


@pytest.mark.django_db
def test_gestor_create_list_view():
    client = APIClient()
    url = reverse("lista_crear_gestores")
    data = {
        "is_superuser": False,
        "rut": "12.345.678-9",
        "first_name": "Nuevo",
        "username": "nuevo_gestor",
        "last_name": "Gestor",
        "telefono": "987654321",
        "email": "nuevo@gestor.com",
        "password": "hash123",
        "admin": False,
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Gestor.objects.count() == 1

    # Test List with search term
    response = client.get(url, {"termino": "Nuevo"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_gestor_detail_update_delete_view():
    gestor = Gestor.objects.create(
        rut="12.345.678-9",
        first_name="Editar",
        last_name="Gestor",
        username="username",
        telefono="987654321",
        email="editar@gestor.com",
        password="hash123",
        admin=False,
    )
    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_gestor", args=[gestor.id])
    data = {
        "rut": "987654321",
        "first_name": "Editado",
        "last_name": "Gestor",
        "username": "username",
        "telefono": "12.345.678-9",
        "email": "editado@gestor.com",
        "password": "hash456",
        "admin": False,
    }

    # Test Read
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Editar"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Gestor.objects.get(id=gestor.id).rut == "987654321"
    assert Gestor.objects.get(id=gestor.id).first_name == "Editado"
    assert Gestor.objects.get(id=gestor.id).telefono == "12.345.678-9"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Gestor.objects.count() == 0

    # Test Read después de Delete (404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update después de Delete (404)
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete después de Delete (404)
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
