"""Pruebas de integración contra una base MySQL exclusiva para tests."""

import os

import pytest

from app import create_app
from config import TestingConfig
from utils.db import mysql


RUN_DB_INTEGRATION = os.getenv("RUN_DB_INTEGRATION", "").strip().lower() in (
    "1", "true", "yes", "on"
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
        pytest.skip(
            "Faltan variables para integración MySQL: " + ", ".join(missing)
        )

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
def product_id(integration_app):
    with integration_app.app_context():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO products (name, price, description)
                VALUES (%s, %s, %s)
                """,
                (
                    "Producto de integración",
                    100.0,
                    "Producto creado para pruebas",
                ),
            )
            mysql.connection.commit()
            product_id = cursor.lastrowid
        finally:
            cursor.close()

    yield product_id

    with integration_app.app_context():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM products WHERE id = %s",
                (product_id,),
            )
            mysql.connection.commit()
        finally:
            cursor.close()


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
