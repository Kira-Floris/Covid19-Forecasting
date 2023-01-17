import pydantic
import datetime
import typing

class UserBase(pydantic.BaseModel):
    email:str
    company:str
    
class UserCreate(UserBase):
    password:str
    
    class Config:
        orm_mode = True
        
class User(UserBase):
    id:int
    token:str
    token_type:str
    date_created:datetime.datetime
    
    class Config:
        orm_mode=True
        
class PasswordReset(pydantic.BaseModel):
    old_password:str
    new_password:str
        