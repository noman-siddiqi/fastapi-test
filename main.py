from fastapi import FastAPI, HTTPException, status, Form, Depends
import psycopg2
from pydantic import BaseModel
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000"
]

data = []
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
conn = psycopg2.connect(
    dbname="postgres",
    host="localhost",
    user="postgres",
    password="postgres",
    port='5432')


class Car(BaseModel):
    car_id: int | None = None
    make: str
    model: str
    year: int

    
# @app.post("/car")
# async def createcar(car: Car):
#     data.append(car.__dict__)
#     cur = conn.cursor()
#     insert_query = "INSERT INTO car (make, model, year) VALUES (%s, %s, %s)"
#     cur.execute(insert_query, (car.make, car.model, car.year))
#     cur.close()
#     conn.commit()

#     return car

@app.post("/car")
async def createcar(car: Car):
    data.append(car.__dict__)
    cur = conn.cursor()
    cur.execute("INSERT INTO car (make, model, year) VALUES (%s, %s, %s) returning car_id", (car.make, car.model, car.year))
    cardata = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return {"car_id": cardata}

@app.get("/cars")
async def get_cars_from_db():   
    cur = conn.cursor()
    cur.execute("SELECT * FROM car")
    columns = cur.description 
    cars = [{columns[index][0]:
            column for index, column in enumerate(value)} 
            for value in cur.fetchall()]
    for car in cars:
        print(car)            
    cur.close()     
    if cars:
        return cars
    else:
        return {"Error message": "car table is empty"}

@app.get("/car/{car_id}")
async def get_cars_by_make(car_id):   
    cur = conn.cursor()
    select_query = "select * from car where car_id = %s"
    cur.execute(select_query, (car_id,))
    cars = cur.fetchone()
    print(cars)
    for car in cars:
        print(car)  
    cur.close()     
    if cars:
        return {
                "car_id": cars[0],
                "make": cars[1],
                "mode": cars[2],
                "year": cars[3]
                }
    else:
        return {"Error message": "car id does not exist"}

@app.put("/car/{car_id}")
async def update_car_by_model(car_id: str, car: Car):   
    cur = conn.cursor()
    update_query = "Update car set model=%s, year=%s where car_id=%s"
    cur.execute(update_query, (car.model, car.year ,car_id))
    conn.commit()
    cur.close()
    return {"message": "updated successfully"}

@app.delete("/car/{car_id}")
async def delete_car_by_model(car_id):   
    cur = conn.cursor()
    delete_query = "DELETE FROM car WHERE car_id=%s"
    cur.execute(delete_query, (car_id,))
    conn.commit()
    cur.close()
    return {"message": "deleted successfully"}

@app.get("/")
async def root():
    return {"message": "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"}


@app.get("/messages")
async def get_all_messagges():
    if len(data) == 0:
        return {"message": "message list is empty"}
    else:
        return {"message": data}


@app.get("/message/message_id")
async def get_message_by_id(message_id: int):
    if len(data) > 0:
        if len(data) > message_id:
            return {"message": data[message_id]}
        else:
            return{"message": str(message_id) + " No data exists on the message id"}
    else:
        return {"message": "Message list is empty"}   


@app.post("/my-message")
async def add_message_in_the_list(msg: str):
	print(f">> {msg}")
	data.append(msg)
	return { "message": "your message " + msg + " has saved in the msg list"}


@app.put("/msg/new_msg")
async def update_message_by_id(msg: str, new_msg: str):
    if len(data) > 0:
        for index in range(len(data)):
            if data[index] == msg:
                data[index] = new_msg
                return {"message": data}
    else:
        return {"message": "No updagte operation - message list is empty"}


@app.delete("/message")
async def delete_all_messages():
    if len(data) > 0:
        data.clear()
        return {"message": "Messages are deleted and size of list is " + str(len(data))}
    else:
        return {"message": "No delete operation - message list is empty"}


@app.delete("/msg")
async def delete_message_by_id(msg: str):
    if len(data) > 0:
        for index in range(len(data)):
            if data[index] == msg:
                data.pop(index)
                return{"message": data}
    else:
        return {"message": "No delete operation - message list is empty"}
    
#
#Query parameters
#
@app.get("/query-params-demo", status_code=status.HTTP_200_OK)
async def query_params(p: str, q: int, r: str | None = None, s: int | None = 7):
        return {
            "message": "OK",
            "p": p,
            "q": q,
            "r": r,
            "s": s
        }
        
#
#Form handling  
#
@app.post("/login/")
async def login_handler(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print('username' + username)
    print('password' + password)       
    
    return  {
        "username": username,
        "password": password
    }    
    
@app.get("/query-params-demo", status_code=status.HTTP_200_OK)
async def get_cars_query_params(p: str, q: int, r: str | None = "my-default-value", s: int | None = 7):
    return {
        "message": "OK",
        'p': p,
        'q': q,
        'r': r,
        's': s
        }
    
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return { "q": q, "skip": skip, "limit": limit}

@app.get("/some-resource1")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/some-resource2")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

#! Standard Python "type alias"
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/some-resource3/")
async def read_items(commons: CommonsDep):
    return commons

@app.get("/some-resource4/")
async def read_users(commons: CommonsDep):
    return commons