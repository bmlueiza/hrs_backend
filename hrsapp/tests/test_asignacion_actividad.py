import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, time
from hrsapp.models.asignacion_actividad import AsignacionActividad
from hrsapp.models.actividad_medica import ActividadMedica
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico

# Modelo


@pytest.mark.django_db
def test_crear_asignacion_actividad():
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
    actividad = ActividadMedica.objects.create(
        nombre="Actividad Test", descripcion="Descripción opcional"
    )
    asignacion = AsignacionActividad.objects.create(
        fecha_asignacion=date.today(),
        fecha_actividad=date.today(),
        hora_actividad=time(10, 0),
        estado=1,  # Asignada
        paciente=paciente,
        actividad_medica=actividad,
    )

    assert AsignacionActividad.objects.count() == 1
    assert asignacion.fecha_asignacion == date.today()
    assert asignacion.fecha_actividad == date.today()
    assert asignacion.hora_actividad == time(10, 0)
    assert asignacion.estado == 1
    assert asignacion.paciente == paciente
    assert asignacion.actividad_medica == actividad


# Views


@pytest.mark.django_db
def test_estado_choices():
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
    actividad = ActividadMedica.objects.create(
        nombre="Actividad Test", descripcion="Descripción opcional"
    )

    # Intentar crear una asignación con un estado no válido debería retornar un 400 Bad Request
    client = APIClient()
    url = reverse("lista_crear_asignacion_actividades")
    data = {
        "fecha_asignacion": str(date.today()),
        "fecha_actividad": str(date.today()),
        "hora_actividad": str(time(10, 0)),
        "estado": 5,  # Estado no válido
        "paciente": paciente.id,
        "actividad_medica": actividad.id,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "estado" in response.data


@pytest.mark.django_db
def test_asignacion_actividad_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_asignacion_actividades")
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
    actividad = ActividadMedica.objects.create(
        nombre="Actividad Test", descripcion="Descripción opcional"
    )
    data = {
        "fecha_asignacion": "2023-01-01",
        "fecha_actividad": "2023-01-02",
        "hora_actividad": "10:00",
        "estado": 1,
        "paciente": paciente.id,
        "actividad_medica": actividad.id,
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert AsignacionActividad.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_asignacion_actividad_detail_update_delete_view():
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
    actividad = ActividadMedica.objects.create(
        nombre="Actividad Test", descripcion="Descripción opcional"
    )
    asignacion = AsignacionActividad.objects.create(
        fecha_asignacion=date.today(),
        fecha_actividad=date.today(),
        hora_actividad=time(10, 0),
        estado=1,
        paciente=paciente,
        actividad_medica=actividad,
    )
    client = APIClient()
    url = reverse(
        "detalle_actualizar_eliminar_asignacion_actividad", args=[asignacion.id]
    )
    data = {
        "fecha_asignacion": "2023-01-01",
        "fecha_actividad": "2023-01-02",
        "hora_actividad": "11:00",
        "estado": 2,  # Cambiando el estado a "Realizada"
        "paciente": paciente.id,
        "actividad_medica": actividad.id,
    }

    # Test Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["hora_actividad"] == "10:00:00"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert AsignacionActividad.objects.get(id=asignacion.id).hora_actividad == time(
        11, 0
    )
    assert AsignacionActividad.objects.get(id=asignacion.id).estado == 2

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert AsignacionActividad.objects.count() == 0

    # Test Retrieve after Delete (should return 404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
