import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
import sqlalchemy

import os
import sys

# print(sys.path)

import settings
from routes import auth, views
from utils import mail as utils_mail
import models
from config.database import SessionLocal

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
app.include_router(auth.router, prefix='/auth')
app.include_router(views.router, prefix='/api')

async def background(session):
    print('Initiating startup process')
    print('--------------------------')
    
    print('\nRETRIEVING DATA')
    print('----------------')
    df = pd.read_csv(settings.DATA_SOURCE)
    print('Data Retrieval Done')
    print('-------------------')
    
    # rename index column to id
    df.index.name = 'id'
    
    # drop columns that are not wanted
    # get wanted list
    df.drop(df.columns.difference(settings.DATA_COLUMNS), axis=1, inplace=True)
    df = df[df['location']==settings.COUNTRY]
    # print(df.head(10))
    
    df.to_csv(settings.DATA_SAVE_FILE)
    print('Data Saving Done')
    print('----------------')
    
    print('\nTRAINING MODELS')
    print('----------------')
    Training()
    print('Training Done')
    print('----------------')
    
    # checking for spikes and sending notifications
    print('\nCHECKING FOR SPIKES')
    print('----------------')
    predictions = pd.read_csv(settings.PREDICTION_SAVE_FILE)
    send_email = False
    for index, row in predictions.iterrows():
        if row['fb_prophet'] > settings.THRESHOLD:
            send_email = True
            break
    if send_email:
        print('Spikes found, sending email notifications.')
        print('----------------')
        await utils_mail.automated_email(predictions, session)
        print('Email notifications sent.')
        print('----------------')
    else:
        print('No Spikes found.')
        print('----------------')
        
    

# load and save data each day for data retrieval speeds
@app.on_event('startup')
@repeat_every(seconds=86400, wait_first=False)
async def retrieve_data():
    # with SessionLocal() as session:
        # await background(session)
    pass


# mounting frontend
# app.mount('/', StaticFiles(directory='client/build', html=True),name='templates')

# running app
if __name__=='__main__':
    print(f"Server hosted at {settings.HOST}:{int(settings.PORT)}")
    app_str = 'main:app'
    uvicorn.run(app_str, host=settings.HOST, port=settings.PORT, reload=True)