import fastapi
from fastapi import security
import pydantic
import sqlalchemy

import sys
sys.path.append('..')

import settings
from schemas import user as schemas_user
from models import user as models_user
from utils import auth as utils_auth

router = fastapi.APIRouter()

@router.post('/user/register')
async def create_user(
    user:schemas_user.UserCreate, 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    
    user = await utils_auth.create_user(user=user, db=session)
    return await utils_auth.create_token(user=user)

@router.post('/token')
async def generate_token(
    form_data:security.OAuth2PasswordRequestForm=fastapi.Depends(),
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    
    user = await utils_auth.authenticate_user(
        email=form_data.username, password=form_data.password, 
        session=session)
    
    if user:
        return await utils_auth.create_token(user=user)
    
@router.get('/user/me')
async def get_user(
    user:schemas_user.User=fastapi.Depends(utils_auth.get_current_user)
    ):
    return user