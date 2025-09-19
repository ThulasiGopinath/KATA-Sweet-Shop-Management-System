import sys
sys.path.append('C:\\Users\\Gopinath\\Documents\\Thulasi\\Incubyte\\kATA')
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}