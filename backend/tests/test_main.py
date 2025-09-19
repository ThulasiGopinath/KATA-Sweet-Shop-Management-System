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