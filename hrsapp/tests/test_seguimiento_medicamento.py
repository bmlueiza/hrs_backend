import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import datetime
from hrsapp.models.seguimiento_medicamento import SeguimientoMedicamento
from hrsapp.models.paciente import Paciente
from hrsapp.models.gestor import Gestor
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.models.medicamento import Medicamento
from hrsapp.models.medico import Medico
from hrsapp.models.especialidad_medica import EspecialidadMedica

# Modelo


@pytest.mark.django_db
def test_crear_seguimiento_medicamento():
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
    especialidad = EspecialidadMedica.objects.create(nombre="Especialidad")
    medico = Medico.objects.create(
        rut="22.222.222-2",
        nombre="Medico",
        apellido="Apellido",
        especialidad=especialidad,
    )
    medicamento = Medicamento.objects.create(
        nombre="Medicamento", descripcion="Descripción opcional"
    )

    seguimiento_medicamento = SeguimientoMedicamento.objects.create(
        fecha_inicio="2020-01-01",
        fecha_termino="2020-01-01",
        cantd_otorgada="30 comprimidos",
        indicacion_uso="1 comprimido cada 8 horas",
        proximo_despacho="2020-01-01",
        estado=1,
        paciente=paciente,
        diagnostico=diagnostico,
        medicamento=medicamento,
        medico=medico,
    )
    assert SeguimientoMedicamento.objects.count() == 1
    assert seguimiento_medicamento.fecha_inicio == "2020-01-01"
    assert seguimiento_medicamento.fecha_termino == "2020-01-01"
    assert seguimiento_medicamento.cantd_otorgada == "30 comprimidos"
    assert seguimiento_medicamento.indicacion_uso == "1 comprimido cada 8 horas"
    assert seguimiento_medicamento.proximo_despacho == "2020-01-01"
    assert seguimiento_medicamento.estado == 1
    assert seguimiento_medicamento.paciente == paciente
    assert seguimiento_medicamento.diagnostico == diagnostico
    assert seguimiento_medicamento.medicamento == medicamento
    assert seguimiento_medicamento.medico == medico
    assert seguimiento_medicamento.medico.especialidad == especialidad


# Views


@pytest.mark.django_db
def test_seguimiento_medicamento_list_create_view():
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
    especialidad = EspecialidadMedica.objects.create(nombre="Especialidad")
    medico = Medico.objects.create(
        rut="22.222.222-2",
        nombre="Medico",
        apellido="Apellido",
        especialidad=especialidad,
    )
    medicamento = Medicamento.objects.create(
        nombre="Medicamento", descripcion="Descripción opcional"
    )
    client = APIClient()
    url = reverse("lista_crear_seguimiento_medicamentos")
    data = {
        "fecha_inicio": "2020-01-01",
        "fecha_termino": "2020-01-01",
        "cantd_otorgada": "30 comprimidos",
        "indicacion_uso": "1 comprimido cada 8 horas",
        "proximo_despacho": "2020-01-01",
        "estado": 1,
        "paciente": paciente.id,
        "diagnostico": diagnostico.id,
        "medicamento": medicamento.id,
        "medico": medico.id,
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_seguimiento_medicamento_detail_update_delete_view():
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
    especialidad = EspecialidadMedica.objects.create(nombre="Especialidad")
    medico = Medico.objects.create(
        rut="22.222.222-2",
        nombre="Medico",
        apellido="Apellido",
        especialidad=especialidad,
    )
    medicamento = Medicamento.objects.create(
        nombre="Medicamento", descripcion="Descripción opcional"
    )
    seguimiento_medicamento = SeguimientoMedicamento.objects.create(
        fecha_inicio="2020-01-01",
        fecha_termino="2020-01-01",
        cantd_otorgada="30 comprimidos",
        indicacion_uso="1 comprimido cada 8 horas",
        proximo_despacho="2020-01-01",
        estado=1,
        paciente=paciente,
        diagnostico=diagnostico,
        medicamento=medicamento,
        medico=medico,
    )

    client = APIClient()
    url = reverse(
        "detalle_actualizar_eliminar_seguimiento_medicamento",
        args=[seguimiento_medicamento.id],
    )
    data = {
        "fecha_inicio": "2020-01-01",
        "fecha_termino": "2020-01-01",
        "cantd_otorgada": "30 comprimidos",
        "indicacion_uso": "1 comprimido cada 8 horas",
        "proximo_despacho": "2020-04-01",
        "estado": 1,
        "paciente": paciente.id,
        "diagnostico": diagnostico.id,
        "medicamento": medicamento.id,
        "medico": medico.id,
    }

    # Test Detail
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    updated_date = datetime.date.fromisoformat(data["proximo_despacho"])
    assert (
        SeguimientoMedicamento.objects.get(
            id=seguimiento_medicamento.id
        ).proximo_despacho
        == updated_date
    )

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Test Detail after Delete (404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update after Delete (404)
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete after Delete (404)
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_seguimiento_medicamento_by_paciente_list_view():
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
    especialidad = EspecialidadMedica.objects.create(nombre="Especialidad")
    medico = Medico.objects.create(
        rut="22.222.222-2",
        nombre="Medico",
        apellido="Apellido",
        especialidad=especialidad,
    )
    medicamento = Medicamento.objects.create(
        nombre="Medicamento", descripcion="Descripción opcional"
    )
    seguimiento_medicamento = SeguimientoMedicamento.objects.create(
        fecha_inicio="2020-01-01",
        fecha_termino="2020-01-01",
        cantd_otorgada="30 comprimidos",
        indicacion_uso="1 comprimido cada 8 horas",
        proximo_despacho="2020-01-01",
        estado=1,
        paciente=paciente,
        diagnostico=diagnostico,
        medicamento=medicamento,
        medico=medico,
    )

    client = APIClient()
    url = reverse("lista_seguimiento_medicamentos_paciente", args=[paciente.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_medicamentos_by_paciente_list_view():
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
    especialidad = EspecialidadMedica.objects.create(nombre="Especialidad")
    medico = Medico.objects.create(
        rut="22.222.222-2",
        nombre="Medico",
        apellido="Apellido",
        especialidad=especialidad,
    )
    medicamento = Medicamento.objects.create(
        nombre="Medicamento", descripcion="Descripción opcional"
    )
    seguimiento_medicamento = SeguimientoMedicamento.objects.create(
        fecha_inicio="2020-01-01",
        fecha_termino="2020-01-01",
        cantd_otorgada="30 comprimidos",
        indicacion_uso="1 comprimido cada 8 horas",
        proximo_despacho="2020-01-01",
        estado=1,
        paciente=paciente,
        diagnostico=diagnostico,
        medicamento=medicamento,
        medico=medico,
    )

    client = APIClient()
    url = reverse("lista_medicamentos_paciente", args=[paciente.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
