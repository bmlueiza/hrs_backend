import json
from rest_framework import status
from hrsapp.models.paciente import Paciente
from hrsapp.models.diagnostico import Diagnostico
from hrsapp.models.gestor import Gestor
from django.urls import reverse
import pytest


@pytest.mark.django_db
@pytest.mark.asyncio
def test_crear_paciente(client):
    # Crear gestor de prueba en la base de datos
    gestor_prueba = Gestor.objects.create(
        rut="12345678-9",
        nombre="NombreGestor",
        apellido="ApellidoGestor",
        telefono="987654321",
        email="gestor@example.com",
        password="password123",
    )

    # Crear diagnósticos de prueba en la base de datos
    diagnostico1 = Diagnostico.objects.create(codigo=1, descripcion="Diagnóstico1")
    diagnostico2 = Diagnostico.objects.create(codigo=2, descripcion="Diagnóstico2")

    url = reverse("crear_paciente")

    # Datos del paciente a crear
    data = {
        "rut": "11111111-1",
        "nombres": "NombrePaciente",
        "apellido1": "Apellido1Paciente",
        "apellido2": "Apellido2Paciente",
        "fecha_nacimiento": "1990-01-01",
        "sexo": "M",
        "telefono": "123456789",
        "direccion": "DirecciónPaciente",
        "alergias": "AlergiasPaciente",
        "diagnosticos": [diagnostico1.id, diagnostico2.id],
        "gestor": gestor_prueba.id,
    }

    # Realizar la solicitud POST
    response = client.post(url, json.dumps(data), content_type="application/json")

    print(response.content.decode("utf-8"))

    # Asegurarse de que la solicitud fue exitosa (código de estado HTTP 201 Created)
    assert response.status_code == status.HTTP_201_CREATED

    # Devolver los objetos de paciente creados
    return Paciente.objects.all()


@pytest.mark.django_db
def test_listar_pacientes(client):
    # Crear pacientes de prueba
    pacientes_creados = test_crear_paciente(client)

    url = reverse("lista_pacientes")

    # Realizar la solicitud GET
    response = client.get(url)

    # Asegurarse de que la solicitud fue exitosa (código de estado HTTP 200 OK)
    assert response.status_code == status.HTTP_200_OK

    # Asegurarse de que la respuesta esté en formato JSON
    assert response.headers["Content-Type"] == "application/json"

    # Asegurarse de que la respuesta contenga la información correcta
    pacientes_en_respuesta = response.json()
    assert len(pacientes_en_respuesta) == len(pacientes_creados)

    assert "rut" in pacientes_en_respuesta[0]
    assert "nombres" in pacientes_en_respuesta[0]
    assert "diagnosticos" in pacientes_en_respuesta[0]

    assert pacientes_en_respuesta[0]["rut"] == str(pacientes_creados[0].rut)
