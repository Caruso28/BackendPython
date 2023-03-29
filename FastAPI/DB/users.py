from pydantic import BaseModel

class User(BaseModel):
    id: str | None #Significa que es opcional
    username: str
    email: str