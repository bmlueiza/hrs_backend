import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.observacion import Observacion
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor

# Modelo


@pytest.mark.django_db
def test_crear_observacion():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    paciente = Paciente.objects.create(
        rut="12.345.678-9",
        nombres="Nuevo",
        apellido1="Paciente",
        apellido2="Apellido",
        fecha_nacimiento="2000-01-01",
        sexo=1,
        telefono="987654321",
        direccion="Dirección de prueba",
        riesgo=1,
        gestor=gestor,
    )
    observacion = Observacion.objects.create(
        contenido="Nueva Observacion",
        fecha_generacion="2021-01-01",
        paciente=paciente,
        gestor=gestor,
    )
    assert Observacion.objects.count() == 1
    assert observacion.contenido == "Nueva Observacion"
    assert observacion.fecha_generacion == "2021-01-01"
    assert observacion.paciente == paciente
    assert observacion.gestor == gestor


# Views


@pytest.mark.django_db
def test_observacion_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_observaciones")
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    paciente = Paciente.objects.create(
        rut="12.345.678-9",
        nombres="Paciente1",
        apellido1="Apellido",
        apellido2="Apellido",
        fecha_nacimiento="2000-01-01",
        sexo=1,
        telefono="12.345.678-9",
        direccion="Dirección de prueba",
        riesgo=1,
        gestor=gestor,
    )
    cliente = APIClient()
    url = reverse("lista_crear_observaciones")
    data = {
        "contenido": "Nueva Observacion",
        "fecha_generacion": "2021-01-01",
        "paciente": paciente.id,
        "gestor": gestor.id,
    }

    # Test Create
    response = cliente.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Test List
    response = cliente.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_observacion_detail_update_delete_view():
    client = APIClient()
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    paciente = Paciente.objects.create(
        rut="12.345.678-9",
        nombres="Paciente1",
        apellido1="Apellido",
        apellido2="Apellido",
        fecha_nacimiento="2000-01-01",
        sexo=1,
        telefono="12.345.678-9",
        direccion="Dirección de prueba",
        riesgo=1,
        gestor=gestor,
    )
    observacion = Observacion.objects.create(
        contenido="Nueva Observacion",
        fecha_generacion="2021-01-01",
        paciente=paciente,
        gestor=gestor,
    )
    client = APIClient()
    url = reverse(
        "detalle_actualizar_eliminar_observacion", kwargs={"pk": observacion.pk}
    )
    data = {
        "contenido": "Nueva Observacion",
        "fecha_generacion": "2021-01-01",
        "paciente": paciente.id,
        "gestor": gestor.id,
    }

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    # Test Detail
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Test Read Not Found
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update Not Found
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete Not Found
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
