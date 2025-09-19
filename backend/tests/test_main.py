import sys
sys.path.append('C:\\Users\\Gopinath\\Documents\\Thulasi\\Incubyte\\kATA')
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_sweets():
    response = client.get("/sweets")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "Gulab Jamun", "price": 1.50},
        {"name": "Jalebi", "price": 2.00},
        {"name": "Rasgulla", "price": 1.75}
    ]

def test_read_chocolates():
    response = client.get("/chocolates")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "KitKat", "price": 1.00},
        {"name": "Dairy Milk", "price": 1.25},
        {"name": "Snickers", "price": 1.50}
    ]

def test_add_sweet():
    sweet_data = {"name": "Laddu", "price": 1.50}
    response = client.post("/add-sweet", json=sweet_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Sweet added successfully"}

def test_update_sweet():
    updated_data = {"name": "Laddu", "price": 2.50}
    response = client.put("/update-sweet", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Sweet updated successfully"}

def test_delete_sweet():
    response = client.delete("/delete-sweet/Laddu")
    assert response.status_code == 200
    assert response.json() == {"message": "Sweet deleted successfully"}

def test_get_sweet_by_id():
    response = client.get("/sweets/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Jalebi", "price": 2.00}