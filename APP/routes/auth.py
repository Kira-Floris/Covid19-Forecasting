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

@router.post('/register')
async def create_user(
    user:schemas_user.UserCreate, 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    
    user = await utils_auth.create_user(user=user, db=session)
    return user

# token should be sent on email
@router.post('/token')
async def generate_token(
    form_data:security.OAuth2PasswordRequestForm=fastapi.Depends(),
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    
    user = await utils_auth.authenticate_user(
        email=form_data.username, password=form_data.password, 
        session=session)
    
    if user:
        return user
    
@router.get('/token/update')
async def update_token(
    request:fastapi.Request,
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    token = request.headers['Authorization']
    user = await utils_auth.check_token(token,session)
    user = await utils_auth.generate_token(user, session)
    return user 
    
@router.get('/me')
async def get_user(
    request:fastapi.Request,
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    token = request.headers['Authorization']
    user = await utils_auth.check_token(token,session)
    return user

@router.get('/test')
async def test(
    blah:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    return {"test":'here we are'}