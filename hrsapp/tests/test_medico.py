import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.medico import Medico

# Modelo


@pytest.mark.django_db
def test_crear_medico():
    medico = Medico.objects.create(
        rut="12.345.678-9",
        nombre="Nuevo Medico",
        apellido="Apellido",
        especialidad="Especialidad",
    )
    assert Medico.objects.count() == 1
    assert medico.rut == "12.345.678-9"
    assert medico.nombre == "Nuevo Medico"
    assert medico.apellido == "Apellido"
    assert medico.especialidad == "Especialidad"


@pytest.mark.django_db
def test_rut_unico_medico():
    Medico.objects.create(
        rut="12.345.678-9",
        nombre="Duplicado",
        apellido="Apellido",
        especialidad="Especialidad",
    )
    with pytest.raises(IntegrityError):
        Medico.objects.create(
            rut="12.345.678-9",
            nombre="Duplicado",
            apellido="Apellido",
            especialidad="Especialidad",
        )


@pytest.mark.django_db
def test_buscar_medicos():
    Medico.objects.create(
        rut="12.345.678-9",
        nombre="Buscar Medico",
        apellido="Apellido",
        especialidad="Especialidad",
    )
    result = Medico.buscar_medicos("Buscar")
    assert result.count() == 1

    result = Medico.buscar_medicos("12.345.678-9")
    assert result.count() == 1

    result = Medico.buscar_medicos("Apellido")
    assert result.count() == 1


@pytest.mark.django_db
def test_buscar_medicos_especialidad():
    Medico.objects.create(
        rut="12.345.678-9",
        nombre="Buscar Medico",
        apellido="Apellido",
        especialidad="Especialidad",
    )
    result = Medico.buscar_medicos_especialidad("Especialidad")
    assert result.count() == 1


# Views


@pytest.mark.django_db
def test_medico_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_medicos")
    data = {
        "rut": "12.345.678-9",
        "nombre": "Nuevo Medico",
        "apellido": "Apellido",
        "especialidad": "Especialidad",
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Medico.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_medico_detail_update_delete_view():
    client = APIClient()
    medico = Medico.objects.create(
        rut="12.345.678-9",
        nombre="Nuevo Medico",
        apellido="Apellido",
        especialidad="Especialidad",
    )
    url = reverse("detalle_actualizar_eliminar_medico", kwargs={"pk": medico.pk})
    data = {
        "rut": "12.345.678-9",
        "nombre": "Nuevo Medico",
        "apellido": "Apellido",
        "especialidad": "Especialidad",
    }

    # Test Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Nuevo Medico"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Nuevo Medico"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Medico.objects.count() == 0

    # Test Read Not Found
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update Not Found
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete Not Found
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
