from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(
    prefix="/usersdb",
    tags=["usersdb"], # para agrupar en la doc
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)


# Get
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Get / Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Get / Query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Post
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya esxiste")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))
        
    return User(**new_user)

# fake body (JSON) para testear POST
# {"username": "sergio", "email": "sergio@fastapi.com"}


# Put
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


# Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el Usuario"}

