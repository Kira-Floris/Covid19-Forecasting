import fastapi
from starlette.middleware.cors import CORSMiddleware
import uvicorn

import os

from routes import auth, views

# setting database
from config.database import Base, engine, SessionLocal
Base.metadata.create_all(engine)

# setting general configuration for the app
app = fastapi.FastAPI(
    title = 'Covid19 Forecasting',
    description = """
    This is a final year project trying to prove covid 19 as seasonal disease and can be forecasted. The project implements machine learning model development, restFUL API to server it and a dashboard to display the results.\n\nThe scope for the project is limited to Rwanda and only covid19 is forecasted as a seasonal disease.""",
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

# running app
if __name__=='__main__':
    port = os.getenv('PORT', default=8000)
    app_str = 'main:app'
    uvicorn.run(app_str, host='0.0.0.0', port=int(port) or 8000, reload=True)