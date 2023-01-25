from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "e59fa8b13820c9428373b2c5de3daa51f9ebf63ea21954a8144df1372d199eaa" # openssl rand -hex 32


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])
# https://bcrypt-generator.com/


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
    "password": "$2a$12$NX/guAtrezeWy1kGn5Huxu2MuhBmF7RGBccszXT0cPF4CJKwYftZ2"
    },
    "elseryei2":{
    "username": "elseryei2",
    "full_name": "Sergio Fogel 2",
    "email": "fogel.sergio2@gmail.com",
    "disabled": True,
    "password": "$2a$12$o9AhqJ..XtkbfoWdp7CXDe.VRZgcLI900ehjUV.D6rkzbFHqGm/ey"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
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

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

# Thunder Client --> POST --> 127.0.0.1:8000/login --> Body --> Form --> Fields: username: elseryei password: 123456


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


