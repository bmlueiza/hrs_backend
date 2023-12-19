import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.actividad_medica import ActividadMedica

# Modelo


@pytest.mark.django_db
def test_crear_actividad_medica():
    actividad = ActividadMedica.objects.create(
        nombre="Nueva Actividad", descripcion="Descripción opcional"
    )
    assert ActividadMedica.objects.count() == 1
    assert actividad.nombre == "Nueva Actividad"
    assert actividad.descripcion == "Descripción opcional"


@pytest.mark.django_db
def test_nombre_unico_actividad_medica():
    ActividadMedica.objects.create(
        nombre="Duplicado", descripcion="Descripción opcional"
    )
    with pytest.raises(IntegrityError):
        ActividadMedica.objects.create(
            nombre="Duplicado", descripcion="Otra descripción"
        )


@pytest.mark.django_db
def test_buscar_actividades():
    ActividadMedica.objects.create(
        nombre="Buscar Actividad", descripcion="Descripción opcional"
    )
    result = ActividadMedica.buscar_actividades("Buscar")
    assert result.count() == 1


# Views


@pytest.mark.django_db
def test_actividad_medica_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_actividades_medicas")
    data = {"nombre": "Nueva Actividad", "descripcion": "Descripción opcional"}

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert ActividadMedica.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_actividad_medica_detail_update_delete_view():
    actividad = ActividadMedica.objects.create(
        nombre="Actividad a Editar", descripcion="Descripción opcional"
    )
    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_actividad_medica", args=[actividad.id])
    data = {"nombre": "Actividad Editada", "descripcion": "Nueva descripción"}

    # Test Read
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Actividad a Editar"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert ActividadMedica.objects.get(id=actividad.id).nombre == "Actividad Editada"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ActividadMedica.objects.count() == 0

    # Test Read después de Delete (404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Update después de Delete (404)
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test Delete después de Delete (404)
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
