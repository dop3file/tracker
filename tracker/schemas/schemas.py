from datetime import date

from pydantic import BaseModel, HttpUrl, Field, EmailStr


class User(BaseModel):
    id: int
    login: str
    email: EmailStr
    password: str
    creation_date: date
   

class SearchQuery(BaseModel):
    artist_name: str | None = None
    
    

