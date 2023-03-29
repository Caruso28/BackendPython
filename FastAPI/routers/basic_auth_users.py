from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "recalculando": {
        "username": "recalculando", 
        "full_name": "Guido Rimati",
        "email": "g_rimati@hotmail.com",
        "disabled": False,
        "password": "123456"
    },

    "recalculando2": {
        "username": "recalculando2",
        "full_name": "Guido Rimato",
        "email": "guidorimati@gmail.com",
        "disabled": True,
        "password": "654321"
    },
}

def search_userdb(username: str):
    if username in users_db:
        return UserDB(**users_db(username))

def search_user(username: str):
    if username in users_db:
        return User(**users_db(username))

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate": "Bearer"})
    return user

    if user.disabled:
        raise HTTPException(
            status_code=400, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    
    user = search_userdb(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")
    
    return {"access_token": user.user_name, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user