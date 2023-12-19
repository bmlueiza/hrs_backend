import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.diagnostico import Diagnostico


@pytest.mark.django_db
def test_crear_diagnostico():
    diagnostico = Diagnostico.objects.create(
        nombre="Nuevo Diagnóstico", codigo="D001", descripcion="Descripción opcional"
    )

    assert Diagnostico.objects.count() == 1
    assert diagnostico.nombre == "Nuevo Diagnóstico"
    assert diagnostico.codigo == "D001"
    assert diagnostico.descripcion == "Descripción opcional"


@pytest.mark.django_db
def test_buscar_diagnosticos():
    Diagnostico.objects.create(
        nombre="Diagnóstico 1", codigo="D001", descripcion="Descripción opcional"
    )
    Diagnostico.objects.create(
        nombre="Diagnóstico 2", codigo="D002", descripcion="Otra descripción"
    )

    # Buscar por nombre
    result = Diagnostico.buscar_diagnosticos("Diagnóstico")
    assert result.count() == 2

    # Buscar por código
    result = Diagnostico.buscar_diagnosticos("D001")
    assert result.count() == 1


@pytest.mark.django_db
def test_diagnostico_create_list_view():
    client = APIClient()
    url = reverse("lista_crear_diagnosticos")
    data = {
        "nombre": "Nuevo Diagnóstico",
        "codigo": "D001",
        "descripcion": "Descripción opcional",
    }

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Diagnostico.objects.count() == 1

    # Test List with search term
    response = client.get(url, {"termino": "Diagnóstico"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_diagnostico_detail_update_delete_view():
    diagnostico = Diagnostico.objects.create(
        nombre="Diagnóstico a Editar", codigo="D001", descripcion="Descripción opcional"
    )
    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_diagnostico", args=[diagnostico.id])
    data = {
        "nombre": "Diagnóstico Editado",
        "codigo": "D002",
        "descripcion": "Nueva descripción",
    }

    # Test Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Diagnóstico a Editar"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Diagnostico.objects.get(id=diagnostico.id).nombre == "Diagnóstico Editado"
    assert Diagnostico.objects.get(id=diagnostico.id).codigo == "D002"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Diagnostico.objects.count() == 0

    # Test Retrieve after Delete (should return 404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
