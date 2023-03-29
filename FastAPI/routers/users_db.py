from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemes.user import user_scheme, users_schema
from db.client  import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

def search_user(id:int):    
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    
# Post

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED) # Por si quiero cambiar el odigo de 200 a 201
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
           status_code=404, detail="El usuario ya existe") #El error se lanza con raise y no con return

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user).inserted_id
    
    new_user = (db_client.users.find_one({"id":id}))
    return User(**new_user)

# Put 

@router.put("/", response_model=User)
async def user(user: User):
        
        user_dict = dict(user)
        del user_dict["id"]
        
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
        
    except:
        return {"error":"No se ha actualizado el usuario"}
                    
    return search_user("_id", ObjectId(user.id))

# Delete

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error":"No se ha eliminado el usuario"}


def search_user(field: str, key):    
    
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_scheme(user))
    except:
        return {"error":"No se ha encontrado el usuario"}
