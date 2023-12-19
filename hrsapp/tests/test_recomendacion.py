import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.recomendacion import Recomendacion
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.models.accion_gestor import AccionGestor

# Modelo


@pytest.mark.django_db
def test_crear_recomendacion():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    diagnostico = Diagnostico.objects.create(
        nombre="Diagnóstico", codigo="D1", descripcion="Descripción opcional"
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
    paciente.diagnosticos.add(diagnostico)
    accion = AccionGestor.objects.create(nombre="Nueva Accion", estado=True)

    recomendacion = Recomendacion.objects.create(
        fecha="2021-01-01",
        tipo_motivo=1,
        motivo="Motivo de prueba",
        paciente=paciente,
        accion_gestor=accion,
    )
    assert Recomendacion.objects.count() == 1
    assert recomendacion.fecha == "2021-01-01"
    assert recomendacion.tipo_motivo == 1
    assert recomendacion.motivo == "Motivo de prueba"
    assert recomendacion.paciente == paciente
    assert recomendacion.accion_gestor == accion


# Views


@pytest.mark.django_db
def test_recomendacion_list_create_view():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    diagnostico = Diagnostico.objects.create(
        nombre="Diagnóstico", codigo="D1", descripcion="Descripción opcional"
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
    paciente.diagnosticos.add(diagnostico)
    accion = AccionGestor.objects.create(nombre="Nueva Accion", estado=True)

    client = APIClient()
    url = reverse("lista_crear_recomendaciones")
    data = {
        "fecha": "2021-01-01",
        "tipo_motivo": 1,
        "motivo": "Motivo de prueba",
        "paciente": paciente.id,
        "accion_gestor": accion.id,
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_recomendacion_detail_update_delete_view():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    diagnostico = Diagnostico.objects.create(
        nombre="Diagnóstico", codigo="D1", descripcion="Descripción opcional"
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
    paciente.diagnosticos.add(diagnostico)
    accion = AccionGestor.objects.create(nombre="Nueva Accion", estado=True)
    recomendacion = Recomendacion.objects.create(
        fecha="2021-01-01",
        tipo_motivo=1,
        motivo="Motivo de prueba",
        paciente=paciente,
        accion_gestor=accion,
    )

    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_recomendacion", args=[recomendacion.id])
    data = {
        "fecha": "2021-01-01",
        "tipo_motivo": 2,
        "motivo": "Motivo de prueba2",
        "paciente": paciente.id,
        "accion_gestor": accion.id,
    }

    # Test Detail
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["tipo_motivo"] == 2
    assert response.data["motivo"] == "Motivo de prueba2"

    # Test Read
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["tipo_motivo"] == 2
    assert response.data["motivo"] == "Motivo de prueba2"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Recomendacion.objects.count() == 0

    # Test Read after Delete (404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update after Delete (404)
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete after Delete (404)
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
