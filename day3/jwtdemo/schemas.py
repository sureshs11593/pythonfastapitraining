from pydantic import BaseModel, EmailStr
# register schema (In)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#login schema
class UserLogin(BaseModel):
    username: str
    password: str

#token shema (In/Out)
class Token(BaseModel):
    access_token:str
    token_type : str

    

    