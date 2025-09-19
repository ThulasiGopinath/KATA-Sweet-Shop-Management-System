from fastapi import FastAPI

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