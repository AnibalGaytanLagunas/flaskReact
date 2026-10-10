"""Pruebas parametrizadas de validación de las rutas de productos."""

import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "", "price": 10, "description": "Válido"},
        {"name": "   ", "price": 10, "description": "Válido"},
        {"name": "Tacos", "price": 0, "description": "Válido"},
        {"name": "Tacos", "price": -1, "description": "Válido"},
        {"name": "Tacos", "price": "no-numérico", "description": "Válido"},
        {"name": "Tacos", "price": 10, "description": ""},
        {"name": "Tacos", "price": 10},
        {
            "name": "Tacos",
            "price": 10,
            "description": "Válido",
            "campo_extra": True,
        },
    ],
)
def test_create_product_rejects_invalid_payload(client, payload):
    response = client.post("/products", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Datos inválidos"


def test_create_product_rejects_malformed_json(client):
    response = client.post(
        "/products",
        data='{"name":',
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Solicitud incorrecta o JSON inválido"}


def test_create_product_requires_json_content_type(client):
    response = client.post(
        "/products",
        data="name=Tacos&price=10&description=Cecina",
    )

    assert response.status_code == 415
    assert response.get_json() == {
        "error": "El contenido debe enviarse como application/json"
    }


def test_update_product_requires_all_fields(client):
    response = client.put(
        "/products/1",
        json={"name": "Tacos", "price": 10},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Datos inválidos"
