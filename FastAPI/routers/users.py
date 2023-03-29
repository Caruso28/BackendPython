from fastapi import APIRouter, HTTPException

router = APIRouter()

# Inicio del server: py -m uvicorn users:app --reload

from pydantic import BaseModel

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Guido", surname="Rimati", url="https://guido.com", age=37),
             User(id=2, name="Arturo", surname="Perro", url="https://arturo.com", age=38),
             User(id=3, name="Tony", surname="Gato", url="https://gato.com", age=39)]

# Get
@router.get("/usersjson")
async def usersjson():
    return [{"Name": "Guido", "Surname": "Rimati", "url": "https://guido.com", "age": 37},
            {"Name": "Arturo", "Surname": "Perro", "url": "https://arturo.com", "age": 38},
            {"Name": "Tony", "Surname": "Gato", "url": "https://gato.com", "age": 39}]

@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

def search_user(id:int):    
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    
# Post

@router.post("/user/", status_code=201) # Por si quiero cambiar el odigo de 200 a 201
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe") #El error se lanza con raise y no con return
    users_list.append(user)
    return user

# Put 

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
        if not found:
            return {"error":"No se ha encontrado el usuario"}
        else:
            return user

# Delete

@router.delete("/user/{id}")
async def user(id: int):
     
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error":"No se ha encontrado el usuario"}


def search_user(id:int):    
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
