import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types.choice import ChoiceType
import datetime
from passlib import hash
import sys

sys.path.append('..')
from config.database import Base


class User(Base):
    __tablename__ = 'User'
    id = sql.Column(sql.Integer, primary_key=True)
    email = sql.Column(sql.String, )
    company = sql.Column(sql.String)
    hashed_password = sql.Column(sql.String)
    date_created = sql.Column(sql.DateTime, default=datetime.datetime.now)
    
    token = sql.Column(sql.String)
    token_type = sql.Column(sql.String, default='bearer')
    
    def verify_password(self, password:str):
        return hash.bcrypt.verify(password, self.hashed_password)
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                