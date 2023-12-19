import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.resultado_contacto import ResultadoContacto

# Modelo


@pytest.mark.django_db
def test_crear_resultado_contacto():
    resultado = ResultadoContacto.objects.create(
        nombre="Nuevo Resultado", descripcion="Descripción opcional"
    )
    assert ResultadoContacto.objects.count() == 1
    assert resultado.nombre == "Nuevo Resultado"
    assert resultado.descripcion == "Descripción opcional"


@pytest.mark.django_db
def test_nombre_unico_resultado_contacto():
    ResultadoContacto.objects.create(
        nombre="Duplicado", descripcion="Descripción opcional"
    )
    with pytest.raises(IntegrityError):
        ResultadoContacto.objects.create(
            nombre="Duplicado", descripcion="Otra descripción"
        )


# Views


@pytest.mark.django_db
def test_resultado_contacto_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_resultados_contacto")
    data = {"nombre": "Nuevo Resultado", "descripcion": "Descripción opcional"}

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert ResultadoContacto.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_resultado_contacto_detail_update_delete_view():
    client = APIClient()
    resultado = ResultadoContacto.objects.create(
        nombre="Nuevo Resultado", descripcion="Descripción opcional"
    )
    url = reverse(
        "detalle_actualizar_eliminar_resultado_contacto", kwargs={"pk": resultado.pk}
    )
    data = {"nombre": "Nuevo Resultado", "descripcion": "Descripción opcional"}

    # Test Detail
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == resultado.nombre

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Nuevo Resultado"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ResultadoContacto.objects.count() == 0

    # Test Read Not Found
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update Not Found
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete Not Found
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
