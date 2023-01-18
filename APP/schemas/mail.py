import pydantic
import datetime
import typing

class ContactBase(pydantic.BaseModel):
    email:str
    subject:str
    message:str