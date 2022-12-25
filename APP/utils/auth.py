from secrets import token_bytes
import sqlalchemy
import passlib.hash as hash

import jwt

import fastapi

import sys
sys.path.append('..')
import models as models
import schemas as schemas
import settings

oauth2schema = settings.get_oauth2schema()

async def get_user_by_email(email:str, db:sqlalchemy.orm.Session):
    return db.query(models.user.User).filter(models.user.User.email==email).first()

async def create_user(user:schemas.user.UserCreate, db:sqlalchemy.orm.Session):
    hashed_password = hash.bcrypt.hash(user.password)
    user_obj = models.user.User(email=user.email, hashed_password=hashed_password)
    
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def create_token(user:models.user.User):
    user_schema_obj = schemas.user.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict['date_created']
    token = jwt.encode(user_dict, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return dict(access_token=token, token_type='bearer')

async def authenticate_user(email:str, password:str, session:sqlalchemy.orm.Session):
    user = await get_user_by_email(email=email, db=session)
    if not user:
        raise fastapi.HTTPException(status=404, detail='User Not Found')
    if not user.verify_password(password):
        raise fastapi.HTTPException(status=401, detail='Invalid Credentials')
    return user

async def get_current_user(token:str=fastapi.Depends(oauth2schema), session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = session.query(models.user.User).get(payload['id'])
    except Exception as error:
        raise fastapi.HTTPException(status_code=401, detail=f'Invalid Credentials with this error:\n {error}')
    return schemas.user.User.from_orm(user)