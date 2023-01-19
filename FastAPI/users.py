from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_fake_db = [
    User(id=1, name="Pedro", surname="Gonzalez", age=32),
    User(id=2, name="Juan", surname="Perez", age=33),
    User(id=3, name="Carlos", surname="Garcia", age=34)]

@app.get("/users")
async def users():
    return users_fake_db

# Path --> 127.0.0.1:8000/user/1
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query --> 127.0.0.1:8000/user/?id=1           más parámetros, concatenar: /user/?id=1&name=Pedro...
@app.get("/user/")
async def user(id: int):
    return search_user(id)

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_fake_db)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el Usuario"}

