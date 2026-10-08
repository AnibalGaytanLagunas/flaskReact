"""Pruebas unitarias de las reglas de negocio de productos."""

from unittest.mock import Mock

import pytest

from exceptions.product_exceptions import ProductNotFoundError
from services import product_service


def test_service_update_product_returns_product(monkeypatch):
    repository = Mock()
    repository.update_product.return_value = True
    monkeypatch.setattr(product_service, "product_repository", repository)

    result = product_service.service_update_product(
        5, " Tacos ", 50.0, " Cecina "
    )

    assert result == {
        "id": 5,
        "name": "Tacos",
        "price": 50.0,
        "description": "Cecina",
    }
    repository.update_product.assert_called_once_with(
        5, "Tacos", 50.0, "Cecina"
    )


def test_service_update_product_raises_not_found(monkeypatch):
    repository = Mock()
    repository.update_product.return_value = False
    monkeypatch.setattr(product_service, "product_repository", repository)

    with pytest.raises(ProductNotFoundError):
        product_service.service_update_product(
            999, "Tacos", 50.0, "Cecina"
        )


def test_service_delete_product_returns_id(monkeypatch):
    repository = Mock()
    repository.delete_product.return_value = True
    monkeypatch.setattr(product_service, "product_repository", repository)

    result = product_service.service_delete_product(5)

    assert result == 5
    repository.delete_product.assert_called_once_with(5)


def test_service_delete_product_raises_not_found(monkeypatch):
    repository = Mock()
    repository.delete_product.return_value = False
    monkeypatch.setattr(product_service, "product_repository", repository)

    with pytest.raises(ProductNotFoundError):
        product_service.service_delete_product(999)
