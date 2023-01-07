import fastapi
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd

import os
import sys

# print(sys.path)

import settings
from routes import auth, views

# setting database
from config.database import Base, engine, SessionLocal
Base.metadata.create_all(engine)

# importing training schedules
from ML.main import main as Training

# setting general configuration for the app
app = fastapi.FastAPI(
    title = 'Covid19 Forecasting',
    description = """
    This is a final year project trying to prove covid 19 as seasonal disease and can be forecasted. The project implements machine learning model development, restFUL API to serve it and a dashboard to display the results.\n\nThe scope for the project is limited to Rwanda and only covid19 is forecasted as a seasonal disease.""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# adding middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# adding routes
app.include_router(auth.router)
app.include_router(views.router)

def background():
    print('Initiating startup process')
    print('--------------------------')
    
    df = pd.read_csv(settings.DATA_SOURCE)
    print('Data Retrieval Done')
    print('-------------------')
    
    # rename index column to id
    df.index.name = 'id'
    
    # drop columns that are not wanted
    # get wanted list
    df.drop(df.columns.difference(settings.DATA_COLUMNS), axis=1, inplace=True)
    # print(df.head(10))
    
    df.to_csv(settings.DATA_SAVE_FILE)
    print('Data Saving Done')
    print('----------------')
    
    print('\n\nTRAINING MODELS')
    print('----------------')
    Training()
    print('Training Done')
    print('----------------')

# load and save data each day for data retrieval speeds
@app.on_event('startup')
@repeat_every(seconds=86400, wait_first=False)
async def retrieve_data():
    # background()
    pass
    

# @app.
    
    

# running app
if __name__=='__main__':
    port = os.getenv('PORT', default=8000)
    app_str = 'main:app'
    uvicorn.run(app_str, host='0.0.0.0', port=int(port) or 8000, reload=True)