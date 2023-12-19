import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.medicamento import Medicamento

# Modelo


@pytest.mark.django_db
def test_crear_medicamento():
    medicamento = Medicamento.objects.create(
        nombre="Nuevo Medicamento", descripcion="Descripción opcional"
    )
    assert Medicamento.objects.count() == 1
    assert medicamento.nombre == "Nuevo Medicamento"
    assert medicamento.descripcion == "Descripción opcional"


@pytest.mark.django_db
def test_nombre_unico_medicamento():
    Medicamento.objects.create(nombre="Duplicado", descripcion="Descripción opcional")
    with pytest.raises(IntegrityError):
        Medicamento.objects.create(nombre="Duplicado", descripcion="Otra descripción")


@pytest.mark.django_db
def test_buscar_medicamentos():
    Medicamento.objects.create(
        nombre="Buscar Medicamento", descripcion="Descripción opcional"
    )
    result = Medicamento.buscar_medicamentos("Buscar")
    assert result.count() == 1


# Views


@pytest.mark.django_db
def test_medicamento_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_medicamentos")
    data = {"nombre": "Nuevo Medicamento", "descripcion": "Descripción opcional"}

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Medicamento.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_medicamento_detail_update_delete_view():
    client = APIClient()
    medicamento = Medicamento.objects.create(
        nombre="Nuevo Medicamento", descripcion="Descripción opcional"
    )
    url = reverse(
        "detalle_actualizar_eliminar_medicamentos", kwargs={"pk": medicamento.id}
    )
    data = {"nombre": "Nuevo Medicamento", "descripcion": "Descripción opcional"}

    # Test Read
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Nuevo Medicamento"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Nuevo Medicamento"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Medicamento.objects.count() == 0
