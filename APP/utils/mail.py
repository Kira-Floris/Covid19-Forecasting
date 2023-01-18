import fastapi_mail
import fastapi
import sqlalchemy
import typing
import pydantic

import sys
sys.path.append('..')
import settings
import models

conf = settings.EMAIL_CONF

class EmailSchema(pydantic.BaseModel):
    email: typing.List[pydantic.EmailStr]
    
def generate_body(df):
    main = """
    <h2>Forecast and Alert on Covid 19 Spikes Notification</h2>
    <p>Our system has detected some rises in covid cases in the near future. Below are the data:</p>
    
    """
    rows = ""
    for index, row in df.iterrows():
        date = row['date']
        prediction = row['fb_prophet']
        rows = rows + f"""
            <b>Date: </b> {date} <br/>
            <b>Predicted Cases: </b>  {int(prediction) if prediction > 0 else 0} cases
            <br/><br/>
        """
    body_end = """
    <p>Take caution and a happy day.</p>
    """
    body = main + rows + body_end
    return body
    
async def automated_email(df, session:sqlalchemy.orm.Session):
    try:
        people = session.query(models.user.User).all()
    except Exception as err:
        print(err)
    recipients = [user.email for user in people]
    message = fastapi_mail.MessageSchema(
        subject = "Forecast and Alert on Covid 19 Spikes Notification",
        recipients = recipients,
        body = generate_body(df),
        subtype= "html"
    )
    
    fm = fastapi_mail.FastMail(conf)
    try:
        response = await fm.send_message(message)
    except Exception as err:
        print('failed: '+err)
        return {"message":"Failed to send emails"}
    finally:
        return {"message":"Emails sent successfully"}
    
async def contact_email(email, subject, body):
    recipients = [email, settings.MAIL_FROM]
    message = fastapi_mail.MessageSchema(
        subject=subject,
        recipients=recipients,
        body=str(body),
        subtype=fastapi_mail.MessageType.plain
    )
    fm = fastapi_mail.FastMail(conf)
    try:
        response = await fm.send_message(message)
    except Exception as err:
        print('failed: '+err)
        return False, "Failed to send emails"
    finally:
        return True, "Emails sent successfully"
    