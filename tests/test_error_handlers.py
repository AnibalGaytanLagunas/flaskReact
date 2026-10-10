import pytest

from exceptions.product_exceptions import (
    ProductNotFoundError,
    ProductCreationError,
    ProductUpdateError,
    ProductDeleteError,
    ProductAlreadyExistsError,
    ProductError
)

from services import product_service


# ---------------------------------------------------------
# 400 - Pydantic ValidationError
# ---------------------------------------------------------

def test_validation_error(client):
    response = client.post(
        "/products",
        json={
            "name": "",
            "price": -10,
            "description": "Producto inválido"
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Datos inválidos"
    assert "details" in data


# ---------------------------------------------------------
# 404 - Endpoint no encontrado
# ---------------------------------------------------------

def test_http_not_found(client):
    response = client.get("/endpoint-que-no-existe")
    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Endpoint no encontrado"
    }


# ---------------------------------------------------------
# 404 - Producto no encontrado
# ---------------------------------------------------------

def test_product_not_found(client, monkeypatch):

    def mock_get_product(product_id):
        raise ProductNotFoundError(
            "Producto no encontrado"
        )

    monkeypatch.setattr(
        product_service,
        "service_get_product",
        mock_get_product
    )

    response = client.get("/products/999")

    assert response.status_code == 404

   


# ---------------------------------------------------------
# 409 - Producto ya existente
# ---------------------------------------------------------

def test_product_already_exists(client, monkeypatch):

    def mock_create_product(name, price, description):
        raise ProductAlreadyExistsError(
            "El producto ya existe"
        )

    monkeypatch.setattr(
        product_service,
        "service_create_product",
        mock_create_product
    )

    response = client.post(
        "/products",
        json={
            "name": "Producto existente",
            "price": 100,
            "description": "Producto"
        }
    )

    assert response.status_code == 409

    assert response.get_json() == {
        "error": "El producto ya existe"
    }


# ---------------------------------------------------------
# 500 - Error al crear producto
# ---------------------------------------------------------

def test_product_creation_error(client, monkeypatch):

    def mock_create_product(name, price, description):
        raise ProductCreationError(
            "Error al crear el producto"
        )

    monkeypatch.setattr(
        product_service,
        "service_create_product",
        mock_create_product
    )

    response = client.post(
        "/products",
        json={
            "name": "Producto",
            "price": 100,
            "description": "Producto de prueba"
        }
    )

    assert response.status_code == 500

    assert response.get_json() == {
        "error": "No fue posible crear el producto"
    }


# ---------------------------------------------------------
# 500 - Error al actualizar producto
# ---------------------------------------------------------

def test_product_update_error(client, monkeypatch):

    def mock_update_product(
        product_id,
        name,
        price,
        description
    ):
        raise ProductUpdateError(
            "Error al actualizar el producto"
        )

    monkeypatch.setattr(
        product_service,
        "service_update_product",
        mock_update_product
    )

    response = client.put(
        "/products/1",
        json={
            "name": "Producto actualizado",
            "price": 150,
            "description": "Producto actualizado"
        }
    )

    assert response.status_code == 500

    assert response.get_json() == {
        "error": "No fue posible actualizar el producto"
    }


# ---------------------------------------------------------
# 500 - Error al eliminar producto
# ---------------------------------------------------------

def test_product_delete_error(client, monkeypatch):

    def mock_delete_product(product_id):
        raise ProductDeleteError(
            "Error al eliminar el producto"
        )

    monkeypatch.setattr(
        product_service,
        "service_delete_product",
        mock_delete_product
    )

    response = client.delete("/products/1")

    assert response.status_code == 500

    assert response.get_json() == {
        "error": "No fue posible eliminar el producto"
    }


# ---------------------------------------------------------
# 500 - ProductError general
# ---------------------------------------------------------

def test_product_error(client, monkeypatch):

    def mock_get_all_products():
        raise ProductError(
            "Error general de producto"
        )

    monkeypatch.setattr(
        product_service,
        "service_get_all_products",
        mock_get_all_products
    )

    response = client.get("/products")

    assert response.status_code == 500

    assert response.get_json() == {
        "error": "Error al procesar la operación de productos"
    }


# ---------------------------------------------------------
# 500 - Error inesperado
# ---------------------------------------------------------

def test_unexpected_error(client, monkeypatch):

    def mock_get_all_products():
        raise Exception("Error inesperado")

    monkeypatch.setattr(
        product_service,
        "service_get_all_products",
        mock_get_all_products
    )

    response = client.get("/products")

    assert response.status_code == 500

    assert response.get_json() == {
        "error": "Error interno del servidor"
    }