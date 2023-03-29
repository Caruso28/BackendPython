from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "asde34" #Codigo

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "123456" # Aca iria la contraseña encriptada
    },

    "recalculando2": {
        "username": "recalculando2",
        "full_name": "Guido Rimato",
        "email": "guidorimati@gmail.com",
        "disabled": True,
        "password": "654321" # Aca iria la contraseña encriptada
    },
}

def search_userdb(username: str):
    if username in users_db:
        return UserDB(**users_db(username))
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db(username))
    
async def auth_user(token:str = Depends(oauth2)):
    
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
            status_code=400, 
            detail="Usuario inactivo")
    
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    
    user = search_userdb(form.username)
    
    crypt.verify(form.password, user.password) # Compara contraseña original con encriptada.
    
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")
    
    expirate = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)
    
    acces_token = {"sub":user.username, "exp":datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user