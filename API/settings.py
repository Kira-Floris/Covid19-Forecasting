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

# DATA Credentials
DATA_SOURCE = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DATA_SAVE_FILE = 'data/covid19.csv'
DATA_COLUMNS = ['date','new_cases','continent','location','iso_code','total_cases','new_cases','new_cases','total_deaths','new_deaths']

# JWT Credentials
JWT_SECRET = 'j2d98h9sad9832hd9h28hq3ei2uhdi2h39871dhj923hd'
JWT_ALGORITHM = 'HS256'