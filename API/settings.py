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
    oath2schema = security.OAuth2PasswordBearer(tokenUrl='/user/token')
    return oath2schema