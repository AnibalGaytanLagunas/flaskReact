"""Pruebas de las rutas administrativas deshabilitadas."""

AUTH_UNAVAILABLE_MESSAGE = "Ruta deshabilitada hasta implementar autenticación"


def test_admin_dashboard_is_unavailable(client):
    response = client.get("/admin")

    assert response.status_code == 503
    assert response.get_json() == {"error": AUTH_UNAVAILABLE_MESSAGE}


def test_login_is_unavailable(client):
    response = client.post("/login", json={})

    assert response.status_code == 503
    assert response.get_json() == {"error": AUTH_UNAVAILABLE_MESSAGE}
