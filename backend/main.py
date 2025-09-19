from fastapi import FastAPI
from pydantic import BaseModel

class Sweet(BaseModel):
    name: str
    price: float

class Chocolate(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sweets")
def read_sweets():
    return [
        {"name": "Gulab Jamun", "price": 1.50},
        {"name": "Jalebi", "price": 2.00},
        {"name": "Rasgulla", "price": 1.75}
    ]

@app.get("/chocolates")
def read_chocolates():
    return [
        {"name": "KitKat", "price": 1.00},
        {"name": "Dairy Milk", "price": 1.25},
        {"name": "Snickers", "price": 1.50}
    ]

@app.post("/add-sweet")
def add_sweet(sweet: Sweet):
    return {"message": "Sweet added successfully"}

@app.put("/update-sweet")
def update_sweet(sweet: Sweet):
    return {"message": "Sweet updated successfully"}

@app.delete("/delete-sweet/{name}")
def delete_sweet(name: str):
    return {"message": "Sweet deleted successfully"}