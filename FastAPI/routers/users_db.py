from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client


router = APIRouter(
    prefix="/usersdb",
    tags=["usersdb"], # para agrupar en la doc
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)


users_fake_db = []


# Get
@router.get("/")
async def users():
    return users_fake_db

# Get / Path --> 127.0.0.1:8000/user/1
@router.get("/{id}")
async def user(id: int):
    return search_user(id)

# Get / Query --> 127.0.0.1:8000/user/?id=1           más parámetros, concatenar: /user/?id=1&name=Pedro...
@router.get("/")
async def user(id: int):
    return search_user(id)


# Post
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

#    if type(search_user(user.id)) == User:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya esxiste")

        user_dict = dict(user)
        del user_dict["id"]

        id = db_client.local.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db_client.local.users.find_one({"_id": id}))
        
        return User(**new_user)

# fake body (JSON) para testear POST
# {"username": "elseryei", "age": 34}


# Put
@router.put("/")
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

# fake body (JSON) para testear PUT
# {"username": "elseryei", "age": 17}


# Delete
@router.delete("/{id}")
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

