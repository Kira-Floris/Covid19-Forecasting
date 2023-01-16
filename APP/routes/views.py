import fastapi
import pydantic
import sqlalchemy

import sys
sys.path.append('..')

import settings
from utils import views as utils_views
from utils import auth as utils_auth

router = fastapi.APIRouter()

@router.get('/data')
async def get_data(
    veriffication:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    data = await utils_views.get_data()
    return {"data":data}

@router.get('/predictions')
async def get_predictions(
    veriffication:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    data = await utils_views.get_predictions()
    return {"data":data}

@router.get('/predictions/line')
async def get_predictions_line(
    veriffication:str=fastapi.Depends(utils_auth.verify_token), 
    session:sqlalchemy.orm.Session=fastapi.Depends(settings.get_session)):
    data = await utils_views.get_line()
    return {"data":data}