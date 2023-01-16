from secrets import token_bytes
import sqlalchemy
import passlib.hash as hash

import jwt

import fastapi
import datetime

import sys
sys.path.append('..')
import models as models
import schemas as schemas
import settings

oauth2schema = settings.get_oauth2schema()

def get_user_by_email(email:str, db:sqlalchemy.orm.Session):
    return db.query(models.user.User).filter(models.user.User.email==email).first()

async def create_user(user:schemas.user.UserCreate, db:sqlalchemy.orm.Session):
    if get_user_by_email(user.email, db):
        return None
    hashed_password = hash.bcrypt.hash(user.password)
    user_dict = user.dict()
    # user_dict['date_created'] = datetime.datetime.now
    del user_dict['password']
    token = jwt.encode(user_dict, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    user_obj = models.user.User(email=user.email, company=user.company, hashed_password=hashed_password, token=token)
    
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return schemas.user.User.from_orm(user_obj)

async def generate_token(user:models.user.User, session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    user_schema_obj = schemas.user.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict['date_created']
    # user_dict['date_created'] = datetime.datetime.now
    del user_dict['token']
    del user_dict['token_type']
    token = jwt.encode(user_dict, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    user.token = token
    # user.date_created = user_dict['date_created']
    session.commit()
    return schemas.user.User.from_orm(user)

async def authenticate_user(email:str, password:str, session:sqlalchemy.orm.Session):
    user = get_user_by_email(email=email, db=session)
    if not user:
        raise fastapi.HTTPException(status=404, detail='User Not Found')
    if not user.verify_password(password):
        raise fastapi.HTTPException(status=401, detail='Invalid Credentials')
    return schemas.user.User.from_orm(user)

async def get_current_user(token:str, session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = get_user_by_email(email=payload['email'], db=session)
    except Exception as error:
        raise fastapi.HTTPException(status_code=401, detail=f'Invalid Credentials with this error:\n {error}')
    return schemas.user.User.from_orm(user)

async def check_token(token:str, session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    token_type = token.split(' ')[0]
    token = token.split(' ')[1]
    user = await get_current_user(token, session)
    return user

# decorator for authentication
async def verify_token(
    request:fastapi.Request,
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)
):
    token = request.headers['Authorization']
    user = await check_token(token,session)
    return user