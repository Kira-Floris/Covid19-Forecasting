import pydantic
import datetime

class UserBase(pydantic.BaseModel):
    email:str
    
class UserCreate(UserBase):
    password:str
    
    class Config:
        orm_mode = True
        
class User(UserBase):
    id:int
    date_created:datetime.datetime
    
    class Config:
        orm_mode=True