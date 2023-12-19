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
        nombre="Nuevo",
        apellido="Gestor",
        telefono="987654321",
        email="nuevo@gestor.com",
        password="hash123",
    )

    assert Gestor.objects.count() == 1
    assert gestor.rut == "12.345.678-9"
    assert gestor.nombre == "Nuevo"
    assert gestor.apellido == "Gestor"
    assert gestor.telefono == "987654321"
    assert gestor.email == "nuevo@gestor.com"
    assert gestor.password == "hash123"


@pytest.mark.django_db
def test_rut_unico_gestor():
    Gestor.objects.create(
        rut="12.345.678-9",
        nombre="Gestor1",
        apellido="Apellido",
        telefono="12.345.678-9",
        email="gestor1@example.com",
        password="hash123",
    )
    with pytest.raises(IntegrityError):
        Gestor.objects.create(
            rut="12.345.678-9",
            nombre="Gestor2",
            apellido="Apellido",
            telefono="987654321",
            email="gestor2@example.com",
            password="hash456",
        )


@pytest.mark.django_db
def test_buscar_gestores():
    Gestor.objects.create(
        rut="12.345.678-9",
        nombre="Buscar",
        apellido="Gestor",
        telefono="12.345.678-9",
        email="buscar@gestor.com",
        password="hash123",
    )
    result = Gestor.buscar_gestores("Buscar")
    assert result.count() == 1


# Views


@pytest.mark.django_db
def test_gestor_create_list_view():
    client = APIClient()
    url = reverse("lista_crear_gestores")
    data = {
        "rut": "12.345.678-9",
        "nombre": "Nuevo",
        "apellido": "Gestor",
        "telefono": "987654321",
        "email": "nuevo@gestor.com",
        "password": "hash123",
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
        nombre="Editar",
        apellido="Gestor",
        telefono="987654321",
        email="editar@gestor.com",
        password="hash123",
    )
    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_gestor", args=[gestor.id])
    data = {
        "rut": "987654321",
        "nombre": "Editado",
        "apellido": "Gestor",
        "telefono": "12.345.678-9",
        "email": "editado@gestor.com",
        "password": "hash456",
    }

    # Test Read
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Editar"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Gestor.objects.get(id=gestor.id).rut == "987654321"
    assert Gestor.objects.get(id=gestor.id).nombre == "Editado"
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
