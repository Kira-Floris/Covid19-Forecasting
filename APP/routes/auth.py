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
    response:fastapi.Response,
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    if user.role:
        if user.role not in models_user.user_roles:
            response.status_code=400
            return {"message":"user role is not valid", "error":"user role is not valid"}
    
    user = await utils_auth.create_user(user=user, db=session)
    if user==None:
        response.status_code = 400
        return {"message":"user with that email already exists", "error":"user with that email already exists"}
    return user

# token should be sent on email
@router.post('/token')
async def generate_token(
    response:fastapi.Response,
    form_data:security.OAuth2PasswordRequestForm=fastapi.Depends(),
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    try:
        user = await utils_auth.authenticate_user(
            email=form_data.username, password=form_data.password, 
            session=session)
        return user
    except:
        response.status_code=404
        return {"message":"check your credentials","error":"check your credentials"}
        
    
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

@router.get('/users')
async def get_users(
    token:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    users = session.query(models_user.User).filter(models_user.User.id!=token.id).all()
    return {"data":users}

@router.get('/users/{id}')
async def get_user(
    id:int,
    response:fastapi.Response,
    token:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    try:
        user = session.query(models_user.User).get(id)
        if user:
            return user
        else:
            response.status_code = 404
            return {"message":"user does not exist","error":"user does not exist"}
    except:
        response.status_code = 404
        return {"message":"user does not exist","error":"user does not exist"}

@router.delete('/users/{id}')
async def delete_user(
    id:int,
    response:fastapi.Response,
    token:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
    ):
    try:
        user = session.query(models_user.User).get(id)
        session.delete(user)
        session.commit()
        return {"message":"user deleted"}
    except:
        response.status_code = 404
        return {"message":"user does not exist","error":"user does not exist"}
    
@router.put('/users/{id}')
async def update_user(
    id:int,
    response:fastapi.Response,
    schema:schemas_user.UserBase,
    token:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
):
    try:
        user = session.query(models_user.User).get(id)
        if schema.email:
            user.email = schema.email
        if schema.company:
            user.company = schema.company
        if schema.role:
            user.role = schema.role
        session.commit()
        return user
    except:
        response.status_code = 400
        return {"message":"bad header","error":"bad header"}
    
@router.put('/reset')
async def update_password(
    request:fastapi.Request,
    response:fastapi.Response,
    schema:schemas_user.PasswordReset,
    token:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
):
    token = request.headers['Authorization']
    user = await utils_auth.check_token(token,session)
    user = session.query(models_user.User).get(user.id)
    check = await utils_auth.change_password(user=user, old_password=schema.old_password, new_password=schema.new_password,db=session)
    if not check:
        response.status_code = 400
        return {"message":"bad header","error":"bad header"}
    return check