"""Pruebas de integración contra una base MySQL exclusiva para tests."""

import os

import pytest

from app import create_app
from config import TestingConfig
from repositories import product_repository
from utils.db import mysql

RUN_DB_INTEGRATION = os.getenv("RUN_DB_INTEGRATION", "").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def integration_app():
    if not RUN_DB_INTEGRATION:
        pytest.skip("Integración MySQL desactivada. Use RUN_DB_INTEGRATION=1.")

    required = (
        "TEST_MYSQL_HOST",
        "TEST_MYSQL_USER",
        "TEST_MYSQL_PASSWORD",
        "TEST_MYSQL_DATABASE",
    )
    missing = [variable for variable in required if not os.getenv(variable)]
    if missing:
        pytest.skip("Faltan variables para integración MySQL: " + ", ".join(missing))

    class IntegrationConfig(TestingConfig):
        SECRET_KEY = os.getenv("TEST_SECRET_KEY", "integration-test-secret")
        MYSQL_HOST = os.getenv("TEST_MYSQL_HOST")
        MYSQL_PORT = int(os.getenv("TEST_MYSQL_PORT", "3306"))
        MYSQL_USER = os.getenv("TEST_MYSQL_USER")
        MYSQL_PASSWORD = os.getenv("TEST_MYSQL_PASSWORD")
        MYSQL_DB = os.getenv("TEST_MYSQL_DATABASE")

    app = create_app(IntegrationConfig)

    with app.app_context():
        yield app


@pytest.fixture
def integration_client(integration_app):
    return integration_app.test_client()


@pytest.fixture
def cleanup_products(integration_app):
    """Elimina al finalizar únicamente los productos registrados por el test."""
    product_ids = []
    yield product_ids.append

    with integration_app.app_context():
        for product_id in product_ids:
            product_repository.delete_product(product_id)


@pytest.fixture
def product_id(integration_app, cleanup_products):
    with integration_app.app_context():
        product_id = product_repository.create_product(
            "Producto de integración",
            100.0,
            "Producto creado para pruebas",
        )

    cleanup_products(product_id)
    return product_id


def test_update_product_integration(integration_client, product_id):
    response = integration_client.put(
        f"/products/{product_id}",
        json={
            "name": "Producto actualizado",
            "price": 150.0,
            "description": "Descripción actualizada",
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == product_id
    assert data["name"] == "Producto actualizado"
    assert data["price"] == 150.0
    assert data["description"] == "Descripción actualizada"


def test_delete_product_integration(integration_client, product_id):
    response = integration_client.delete(f"/products/{product_id}")

    assert response.status_code == 200

    get_response = integration_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_create_product_integration(integration_client, cleanup_products):
    product_name = "Producto integración"

    response = integration_client.post(
        "/products",
        json={
            "name": product_name,
            "price": 123.45,
            "description": "Verificación de persistencia",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"]
    cleanup_products(data["id"])
    assert data["name"] == product_name

    get_response = integration_client.get(f"/products/{data['id']}")
    assert get_response.status_code == 200
    assert get_response.get_json()["name"] == product_name


def test_products_table_uses_innodb(integration_app):
    with integration_app.app_context():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT ENGINE
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                """,
                ("products",),
            )
            result = cursor.fetchone()
        finally:
            cursor.close()

    assert result is not None
    assert result[0].lower() == "innodb"
