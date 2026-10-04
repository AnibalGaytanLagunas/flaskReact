"""Reglas de negocio para operaciones de productos."""

from repositories import product_repository
from exceptions.product_exceptions import (
    ProductAlreadyExistsError,
    ProductCreationError,
    ProductDeleteError,
    ProductError,
    ProductNotFoundError,
    ProductUpdateError,
    ProductValidationError,
)


def _validate_product(name, price, description):
    if not isinstance(name, str) or not name.strip():
        raise ProductValidationError("El nombre del producto es obligatorio")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        raise ProductValidationError("El precio debe ser mayor que cero")
    if not isinstance(description, str) or not description.strip():
        raise ProductValidationError("La descripción del producto es obligatoria")


def _product_to_dict(product):
    """Normaliza la fila devuelta por el repositorio a un objeto JSON."""
    if isinstance(product, dict):
        return product
    if isinstance(product, (tuple, list)) and len(product) >= 4:
        return {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "description": product[3],
        }
    raise ProductError("El repositorio devolvió un producto con formato inesperado")


def service_get_all_products():
    try:
        products = product_repository.get_all_products()
        return [_product_to_dict(product) for product in products]
    except ProductError:
        raise
    except Exception as error:
        raise ProductError("No fue posible consultar los productos") from error


def service_create_product(name, price, description):
    _validate_product(name, price, description)
    name = name.strip()
    description = description.strip()

    try:
        product_id = product_repository.create_product(name, price, description)
    except ProductAlreadyExistsError:
        raise
    except Exception as error:
        raise ProductCreationError() from error

    return {
        "id": product_id,
        "name": name,
        "price": price,
        "description": description,
    }


def service_get_product(product_id):
    try:
        product = product_repository.get_product_by_id(product_id)
    except Exception as error:
        raise ProductError("No fue posible consultar el producto") from error

    if product is None:
        raise ProductNotFoundError(product_id)
    return _product_to_dict(product)


def service_update_product(product_id, name, price, description):
    _validate_product(name, price, description)
    name = name.strip()
    description = description.strip()

    try:
        existing_product = product_repository.get_product_by_id(product_id)
    except Exception as error:
        raise ProductError("No fue posible consultar el producto") from error

    if existing_product is None:
        raise ProductNotFoundError(product_id)

    try:
        product_repository.update_product(product_id, name, price, description)
    except ProductAlreadyExistsError:
        raise
    except Exception as error:
        raise ProductUpdateError() from error

    return {
        "id": product_id,
        "name": name,
        "price": price,
        "description": description,
    }


def service_delete_product(product_id):
    try:
        product = product_repository.get_product_by_id(product_id)
    except Exception as error:
        raise ProductError("No fue posible consultar el producto") from error

    if product is None:
        raise ProductNotFoundError(product_id)

    try:
        product_repository.delete_product(product_id)
    except Exception as error:
        raise ProductDeleteError() from error
    return product_id
