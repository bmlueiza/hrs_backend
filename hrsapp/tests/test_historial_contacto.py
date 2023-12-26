import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import datetime
from hrsapp.models.historial_contacto import HistorialContacto
from hrsapp.models.paciente import Paciente
from hrsapp.models.accion_gestor import AccionGestor
from hrsapp.models.resultado_contacto import ResultadoContacto
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico


# Modelo


@pytest.mark.django_db
def test_crear_historial_contacto():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        first_name="Gestor",
        last_name="Apellido",
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
    resultado = ResultadoContacto.objects.create(
        nombre="Nuevo Resultado", descripcion="Descripción opcional"
    )
    historial_contacto = HistorialContacto.objects.create(
        fecha="2021-01-01",
        hora="12:00",
        tipo_motivo=1,
        motivo="Motivo de prueba",
        accion_gestor=accion,
        resultado_contacto=resultado,
        paciente=paciente,
        gestor=gestor,
    )
    assert HistorialContacto.objects.count() == 1
    assert historial_contacto.fecha == "2021-01-01"
    assert historial_contacto.hora == "12:00"
    assert historial_contacto.tipo_motivo == 1
    assert historial_contacto.motivo == "Motivo de prueba"
    assert historial_contacto.accion_gestor == accion
    assert historial_contacto.resultado_contacto == resultado
    assert historial_contacto.paciente == paciente
    assert historial_contacto.gestor == gestor


# Views


@pytest.mark.django_db
def test_historial_contacto_list_create_view():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        first_name="Gestor",
        last_name="Apellido",
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
    resultado = ResultadoContacto.objects.create(
        nombre="Nuevo Resultado", descripcion="Descripción opcional"
    )
    client = APIClient()
    url = reverse("lista_crear_historial_contactos")
    data = {
        "fecha": "2021-01-01",
        "hora": "12:00",
        "tipo_motivo": 1,
        "motivo": "Motivo de prueba",
        "accion_gestor": accion.id,
        "resultado_contacto": resultado.id,
        "paciente": paciente.id,
        "gestor": gestor.id,
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_historial_contacto_detail_update_delete_view():
    gestor = Gestor.objects.create(
        rut="11.111.111-1",
        first_name="Gestor",
        last_name="Apellido",
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
    resultado = ResultadoContacto.objects.create(
        nombre="Nuevo Resultado", descripcion="Descripción opcional"
    )
    historial_contacto = HistorialContacto.objects.create(
        fecha="2021-01-01",
        hora="12:00",
        tipo_motivo=1,
        motivo="Motivo de prueba",
        accion_gestor=accion,
        resultado_contacto=resultado,
        paciente=paciente,
        gestor=gestor,
    )

    client = APIClient()
    url = reverse(
        "detalle_actualizar_eliminar_historial_contacto", args=[historial_contacto.id]
    )
    data = {
        "fecha": "2021-01-04",
        "hora": "14:00",
        "tipo_motivo": 1,
        "motivo": "Motivo de prueba",
        "accion_gestor": accion.id,
        "resultado_contacto": resultado.id,
        "paciente": paciente.id,
        "gestor": gestor.id,
    }

    # Test Detail
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    updated_date = datetime.date.fromisoformat("2021-01-04")
    updated_time = datetime.datetime.strptime("14:00", "%H:%M").time()

    assert HistorialContacto.objects.get(id=historial_contacto.id).fecha == updated_date
    assert HistorialContacto.objects.get(id=historial_contacto.id).hora == updated_time

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert HistorialContacto.objects.count() == 0

    # Test Read after Delete (404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update after Delete (404)
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete after Delete (404)
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
