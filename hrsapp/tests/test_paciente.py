import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico


# Modelo
@pytest.mark.django_db
def test_crear_paciente():
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

    assert Paciente.objects.count() == 1
    assert paciente.rut == "12.345.678-9"
    assert paciente.nombres == "Nuevo"
    assert paciente.apellido1 == "Paciente"
    assert paciente.apellido2 == "Apellido"
    assert str(paciente.fecha_nacimiento) == "2000-01-01"
    assert paciente.sexo == 1
    assert paciente.telefono == "987654321"
    assert paciente.direccion == "Dirección de prueba"
    assert paciente.riesgo == 1
    assert paciente.gestor == gestor
    assert diagnostico in paciente.diagnosticos.all()


@pytest.mark.django_db
def test_rut_unico_paciente():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    Paciente.objects.create(
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
    with pytest.raises(IntegrityError):
        Paciente.objects.create(
            rut="12.345.678-9",
            nombres="Paciente2",
            apellido1="Apellido",
            apellido2="Apellido",
            fecha_nacimiento="2000-01-01",
            sexo=1,
            telefono="987654321",
            direccion="Dirección de prueba",
            riesgo=1,
            gestor=gestor,
        )


@pytest.mark.django_db
def test_buscar_pacientes():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        nombre="Gestor",
        apellido="Apellido",
        telefono="123456789",
        email="gestor@example.com",
        password="hash123",
    )
    Paciente.objects.create(
        rut="12.345.678-9",
        nombres="Buscar",
        apellido1="Paciente",
        apellido2="Apellido",
        fecha_nacimiento="2000-01-01",
        sexo=1,
        telefono="12.345.678-9",
        direccion="Dirección de prueba",
        riesgo=1,
        gestor=gestor,
    )
    Paciente.objects.create(
        rut="19.345.678-9",
        nombres="Otro",
        apellido1="Paciente",
        apellido2="Apellido",
        fecha_nacimiento="2000-01-01",
        sexo=1,
        telefono="12.345.678-9",
        direccion="Dirección de prueba",
        riesgo=1,
        gestor=gestor,
    )
    result = Paciente.buscar_pacientes("Buscar")
    assert result.count() == 1

    result = Paciente.buscar_pacientes("12.345.678-9")
    assert result.count() == 1

    result = Paciente.buscar_pacientes("Paciente")
    assert result.count() == 2


# Views
@pytest.mark.django_db
def test_paciente_create_list_view():
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
    diagnostico2 = Diagnostico.objects.create(
        nombre="Diagnóstico2", codigo="D2", descripcion="Descripción opcional"
    )
    client = APIClient()
    url = reverse("lista_crear_pacientes")
    data = {
        "rut": "12.345.678-9",
        "nombres": "Nuevo",
        "apellido1": "Paciente",
        "apellido2": "Apellido",
        "fecha_nacimiento": "2000-01-01",
        "sexo": 1,
        "telefono": "987654321",
        "direccion": "Dirección de prueba",
        "riesgo": 1,
        "gestor": gestor.id,
        "diagnosticos": [diagnostico.id, diagnostico2.id],
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Paciente.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Test Search
    response = client.get(url, {"termino": "Nuevo"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_paciente_detail_update_delete_view():
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
        nombres="Editar",
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

    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_paciente", args=[paciente.id])
    data = {
        "rut": "98.765.432-1",
        "nombres": "Editado",
        "apellido1": "Paciente",
        "apellido2": "Apellido",
        "fecha_nacimiento": "2000-01-01",
        "sexo": 1,
        "telefono": "123456789",
        "direccion": "Dirección de prueba",
        "riesgo": 2,
        "gestor": gestor.id,
        "diagnosticos": [diagnostico.id],
    }

    # Test Read
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombres"] == "Editar"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Paciente.objects.get(id=paciente.id).rut == "98.765.432-1"
    assert Paciente.objects.get(id=paciente.id).nombres == "Editado"
    assert Paciente.objects.get(id=paciente.id).telefono == "123456789"
    assert Paciente.objects.get(id=paciente.id).riesgo == 2

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Paciente.objects.count() == 0

    # Test Read after Delete (404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update after Delete (404)
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete after Delete (404)
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Search after Delete (404)
    response = client.get(url, {"termino": "Editar"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
