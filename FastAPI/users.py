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


# Get
@app.get("/users")
async def users():
    return users_fake_db

# Get / Path --> 127.0.0.1:8000/user/1
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Get / Query --> 127.0.0.1:8000/user/?id=1           más parámetros, concatenar: /user/?id=1&name=Pedro...
@app.get("/user/")
async def user(id: int):
    return search_user(id)


# Post
@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya esxiste"}
    else:
        users_fake_db.append(user)
        return user

# fake JSON para testear POST
# {"id": 4, "name": "Sergio", "surname": "Fogel", "age": 34}


# Put
@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el Usuario"}
    else:
        return user

# fake JSON para testear PUT
# {"id": 4, "name": "Sergio", "surname": "Fogel", "age": 18}


# Delete
@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}

# /user/4


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_fake_db)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el Usuario"}

