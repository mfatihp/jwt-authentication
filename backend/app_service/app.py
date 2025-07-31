from fastapi import FastAPI
from fastapi import HTTPException, status
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.schemas import Payload, NewUser
from utils.signup_manager import SignupManager

import os
import jwt

load_dotenv()

app = FastAPI()
sign_up_mng = SignupManager()



def check_token_validity(token:str):
    payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])
    exp_timestamp = payload.get("exp")
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=ZoneInfo("Europe/Istanbul"))
    
    # Check expiration date 
    if exp_datetime > datetime.now(ZoneInfo("Europe/Istanbul")):
        return True, payload.get("sub")
    else: 
        return False, None



@app.get("/awesome_app")
async def ai_function(data: Payload):
    valid, username = check_token_validity(token=data.access_token)

    if valid:
        return {"accessed_user": sign_up_mng.test_db(user_info=username), "msg": "You accessed!!!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    


@app.put("/sync_user")
async def sync(user: NewUser):
    sign_up_mng.sign_up(user_info=user)