import os
import sys

import fastapi_mail

# generating session to query through the model
from config.database import SessionLocal

def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception as error:
        print('Unable to query with this error:\n\t{error}')
    finally:
        session.close()

# creating security reqs
from fastapi import security  
def get_oauth2schema():
    oath2schema = security.OAuth2PasswordBearer(tokenUrl='token', auto_error=False)
    return oath2schema

# DATA information
COUNTRY = 'Rwanda'
ISO_CODE = 'RWA'
DATA_SOURCE = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DATA_SAVE_FILE = './data/covid19.csv'
PREDICTION_SAVE_FILE = './data/covid19-future-values.csv'
PREDICTION_LINE_FILE = './data/covid19-future-values_line.csv'
DATA_COLUMNS = ['date','location','iso_code','new_cases','new_deaths']
THRESHOLD = 100

# JWT Credentials
JWT_SECRET = 'j2d98h9sad9832hd9h28hq3ei2uhdi2h39871dhj923hd'
JWT_ALGORITHM = 'HS256'

# server settings
PORT = int(os.getenv('PORT', default=8000)) or 8000
HOST = '0.0.0.0'

# email settings
EMAIL_CONF = fastapi_mail.ConnectionConfig(
    MAIL_USERNAME = 'nzafloris',
    MAIL_PASSWORD = 'sikrksaaxuzhfuru',
    MAIL_FROM = 'nzafloris@gmail.com',
    MAIL_PORT = 587,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    # USE_CREDENTIALS = True,
    # VALIDATE_CERTS = True
)