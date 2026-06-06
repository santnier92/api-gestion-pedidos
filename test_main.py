from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_inicio():
    response = client.get("/")
    assert response.status_code == 200
    assert "Plataforma de Gestión de Pedidos" in response.json()["mensaje"]

def test_crear_y_listar_pedido():
    # Probar creación
    payload = {
        "cliente": "Santiago Toro",
        "productos": ["Laptop", "Mouse"],
        "cantidades": [1, 2],
        "direccion_envio": "Calle 10 #45-20"
    }
    response = client.post("/pedidos", json=payload)
    assert response.status_code == 200
    assert response.json()["estado"] == "Pendiente"
    assert response.json()["id"] == 1

    # Probar listado
    response_list = client.get("/pedidos")
    assert response_list.status_code == 200
    assert len(response_list.json()) == 1