import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hrsapp.models.accion_gestor import AccionGestor

# Modelo


@pytest.mark.django_db
def test_crear_accion_gestor():
    accion = AccionGestor.objects.create(nombre="Nueva Accion", estado=True)
    assert AccionGestor.objects.count() == 1
    assert accion.nombre == "Nueva Accion"
    assert accion.estado is True


@pytest.mark.django_db
def test_nombre_unico_constraint():
    AccionGestor.objects.create(nombre="Duplicado", estado=True)
    with pytest.raises(IntegrityError):
        AccionGestor.objects.create(nombre="Duplicado", estado=True)


@pytest.mark.django_db
def test_buscar_acciones():
    AccionGestor.objects.create(nombre="Buscar Accion", estado=True)
    result = AccionGestor.buscar_acciones("Buscar")
    assert result.count() == 1


# Views


@pytest.mark.django_db
def test_accion_gestor_list_create_view():
    client = APIClient()
    url = reverse("lista_crear_acciones_gestor")
    data = {"nombre": "Nueva Accion", "estado": True}

    # Test Create
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert AccionGestor.objects.count() == 1

    # Test List
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_accion_gestor_detail_update_delete_view():
    accion = AccionGestor.objects.create(nombre="Accion a Editar", estado=True)
    client = APIClient()
    url = reverse("detalle_actualizar_eliminar_accion_gestor", args=[accion.id])
    data = {"nombre": "Accion Editada", "estado": False}

    # Test Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Accion a Editar"

    # Test Update
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert AccionGestor.objects.get(id=accion.id).nombre == "Accion Editada"

    # Test Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert AccionGestor.objects.count() == 0


# Integración


@pytest.mark.django_db
def test_accion_gestor_workflow():
    # Crear una AccionGestor
    client = APIClient()
    url = reverse("lista_crear_acciones_gestor")
    data = {"nombre": "Nueva Accion", "estado": True}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    accion_id = response.data["id"]

    # Obtener y verificar la AccionGestor recién creada
    url = reverse("detalle_actualizar_eliminar_accion_gestor", args=[accion_id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Nueva Accion"

    # Actualizar la AccionGestor
    data = {"nombre": "Accion Actualizada", "estado": False}
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    # Verificar que la AccionGestor se haya actualizado correctamente
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nombre"] == "Accion Actualizada"

    # Eliminar la AccionGestor
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que la AccionGestor se haya eliminado correctamente
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Verificar que no se pueda eliminar una accion inexistente
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Verificar que no se pueda actualizar una accion inexistente
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Verificar que no se pueda obtener una accion inexistente
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
