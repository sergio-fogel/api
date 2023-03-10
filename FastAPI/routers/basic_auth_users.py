from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# Entidad user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Entidad user db
class UserDB(User): # hereda de User
    password: str


users_db = {
    "elseryei":{
    "username": "elseryei",
    "full_name": "Sergio Fogel",
    "email": "fogel.sergio@gmail.com",
    "disabled": False,
    "password": 123456
    },
    "elseryei2":{
    "username": "elseryei2",
    "full_name": "Sergio Fogel 2",
    "email": "fogel.sergio2@gmail.com",
    "disabled": True,
    "password": 654321
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"}
            )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
            )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

# Thunder Client --> POST --> 127.0.0.1:8000/login --> Body --> Form --> Fields: username: elseryei password: 123456


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

# Thender Client --> GET --> 127.0.0.1:8000/users/me --> Auth --> Bearer --> Token: elseryei


