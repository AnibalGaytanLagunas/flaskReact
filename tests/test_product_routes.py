from exceptions.product_exceptions import * 

def test_new_product_success(client, monkeypatch):
    def mock_create_product(name,price,description):
      return {
        "id": 10,
        "name": name,
        "price": price,
        "description": description
      } 
    monkeypatch.setattr(
        "routes.products_routes.product_service.service_create_product",
        mock_create_product
    )
    response = client.post(
        "/products",
        json={
            "name": "Hamburguesa",
            "price": 120,
            "description": "Hamburguesa con queso"
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 10
    assert data["name"] == "Hamburguesa"
    assert data["price"] == 120
    assert data["description"] == "Hamburguesa con queso"