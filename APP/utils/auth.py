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

def get_user_by_id(id:int, db:sqlalchemy.orm.Session):
    try:
        user = db.query(models.user.User).get(id)
        if user:
            return user
        else:
            raise fastapi.HTTPException(status_code=404, detail=f'user does not exist')
    except:
        raise fastapi.HTTPException(status_code=404, detail=f'user does not exist')
    
async def change_password(user, old_password, new_password, db:sqlalchemy.orm.Session):
    # check if old password is valid
    if not user.verify_password(old_password):
        return None
    hashed_password = hash.bcrypt.hash(new_password)
    
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return user

async def create_user(user:schemas.user.UserCreate, db:sqlalchemy.orm.Session):
    if get_user_by_email(user.email, db):
        return None
    role = user.role if user.role=='admin' else 'user'
    hashed_password = hash.bcrypt.hash(user.password)
    user_dict = user.dict()
    # user_dict['date_created'] = datetime.datetime.now
    del user_dict['password']
    user_obj = models.user.User(email=user.email, company=user.company, hashed_password=hashed_password, role=role, token="")
    
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    user_schema_obj = schemas.user.User.from_orm(user_obj)
    temp_dict = {
        "id":user_schema_obj.id,
        "date_created":str(user_schema_obj.date_created)
    }
    token = jwt.encode(temp_dict, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    user_obj.token = token
    db.commit()
    db.refresh(user_obj)
    return schemas.user.User.from_orm(user_obj)

async def generate_token(user:models.user.User, session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    time_ = datetime.datetime.now()
    user_dict = {
        "id":user.id,
        "datetime":str(time_)
    }
    print(user_dict)
    token = jwt.encode(user_dict, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    user.token = token
    user.date_created = time_
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
        user = get_user_by_id(id=payload['id'], db=session)
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