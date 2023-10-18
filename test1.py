from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
data = []

class Car(BaseModel):
    make: str
    mode: str
    model_year: int
    
@app.post("/car")
def create_car(car: Car):
    data.append(car.dict())
    return data


