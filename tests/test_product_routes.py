"""Pruebas de las rutas HTTP de productos."""

from exceptions.product_exceptions import ProductNotFoundError


def _product(product_id=10, name="Hamburguesa", price=120, description="Con queso"):
    return {
        "id": product_id,
        "name": name,
        "price": price,
        "description": description,
    }


def test_new_product_success(client, monkeypatch):
    def mock_create_product(name, price, description):
        return _product(name=name, price=price, description=description)

    monkeypatch.setattr(
        "routes.products_routes.product_service.service_create_product",
        mock_create_product,
    )
    response = client.post(
        "/products",
        json={
            "name": "Hamburguesa",
            "price": 120,
            "description": "Con queso",
        },
    )

    assert response.status_code == 201
    assert response.get_json() == _product()


def test_read_all_products_success(client, monkeypatch):
    products = [_product(), _product(11, "Tacos", 50, "Cecina")]
    monkeypatch.setattr(
        "routes.products_routes.product_service.service_get_all_products",
        lambda: products,
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert response.get_json() == products


def test_read_all_products_empty(client, monkeypatch):
    monkeypatch.setattr(
        "routes.products_routes.product_service.service_get_all_products",
        lambda: [],
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_product_by_id_success(client, monkeypatch):
    monkeypatch.setattr(
        "routes.products_routes.product_service.service_get_product",
        lambda product_id: _product(product_id=product_id),
    )

    response = client.get("/products/10")

    assert response.status_code == 200
    assert response.get_json() == _product()


def test_get_product_by_id_not_found(client, monkeypatch):
    def mock_get_product(product_id):
        raise ProductNotFoundError(product_id)

    monkeypatch.setattr(
        "routes.products_routes.product_service.service_get_product",
        mock_get_product,
    )

    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "El producto con id 999 no existe"
    }


def test_update_product_success(client, monkeypatch):
    monkeypatch.setattr(
        "routes.products_routes.product_service.service_update_product",
        lambda product_id, name, price, description: _product(
            product_id, name, price, description
        ),
    )

    response = client.put(
        "/products/10",
        json={"name": "Tacos", "price": 50, "description": "Cecina"},
    )

    assert response.status_code == 200
    assert response.get_json() == _product(10, "Tacos", 50, "Cecina")


def test_delete_product_success(client, monkeypatch):
    monkeypatch.setattr(
        "routes.products_routes.product_service.service_delete_product",
        lambda product_id: product_id,
    )

    response = client.delete("/products/10")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Producto eliminado"}
