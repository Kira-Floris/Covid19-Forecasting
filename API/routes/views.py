import fastapi
import pydantic
import sqlalchemy

import sys
sys.path.append('..')

import settings
from utils import views as utils_views

router = fastapi.APIRouter()

@router.get('/data')
async def get_data():
    data = await utils_views.get_data()
    return data